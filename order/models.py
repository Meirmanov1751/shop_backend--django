from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from shop.models import Shop, ShopItem

class Order(models.Model):
  class SHOP_ORDER_STATUSES:
    PROCEED = 'proceed'
    PENDING = 'pending'
    FINISHED = 'finished'
    CANCELED = 'canceled'
    CHOICES = [(PROCEED, 'Готов к выдаче'), (PENDING, 'pending'), (CANCELED, 'Отменен'), (FINISHED, 'Завершен'),
               ]

  class PAYMENT_STATUSES:
    WAITING_FOR_PAYMENT = 'waiting_for_payment'
    PAID = 'paid'
    PARTIALLY_PAID = 'partially_paid'
    CANCELED = 'canceled'
    CHOICES = [(WAITING_FOR_PAYMENT, 'Ожидает оплаты'), (PAID, 'Оплачено'), (CANCELED, 'Отменено'),
               (PARTIALLY_PAID, 'Оплачено частично (только бонусами)')]

  payment_status = models.CharField(max_length=300, choices=PAYMENT_STATUSES.CHOICES,
                                    default=PAYMENT_STATUSES.WAITING_FOR_PAYMENT, verbose_name='Статус оплаты')
  status = models.CharField(choices=SHOP_ORDER_STATUSES.CHOICES, default=SHOP_ORDER_STATUSES.PROCEED, max_length=300,
                            verbose_name='Статус заказа')
  shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
  #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
  preferred_pickup_date = models.DateTimeField(null=True, blank=True, verbose_name='Предпочитаемая дата выдачи')
  total_price = models.IntegerField(default=0, verbose_name='Полная сумма')
  use_bonus = models.BooleanField(default=False, verbose_name='Использовать бонусы для оплаты?')
  price_without_bonus = models.IntegerField(default=0, verbose_name='Цена после списания бонусов')
  created_date = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания заказа')
  qr_code = models.CharField(max_length=500, null=True, blank=True, verbose_name='QR-code')
  end_date = models.DateTimeField(verbose_name='Дата завершения заказа', null=True, blank=True)

  def get_status(self):
    status = self.status
    for choice in self.SHOP_ORDER_STATUSES.CHOICES:
      if status == choice[0]:
        return choice[1]
    return None

  class Meta:
    verbose_name = 'Транзакция заказа'
    verbose_name_plural = 'Транзакция заказа'

  def __init__(self, *args, **kwargs):
    super(Order, self).__init__(*args, **kwargs)
    self.__original_status = self.status

  def save(self, force_insert=False, force_update=False, *args, **kwargs):
    if self.status != self.__original_status:
      if self.status == Order.SHOP_ORDER_STATUSES.CANCELED or self.status == Order.SHOP_ORDER_STATUSES.FINISHED:
        self.end_date = timezone.now()
      if self.__original_status != Order.SHOP_ORDER_STATUSES.PENDING and self.status == Order.SHOP_ORDER_STATUSES.CANCELED:
        self.return_items()
      if self.__original_status != Order.SHOP_ORDER_STATUSES.CANCELED and self.status == Order.SHOP_ORDER_STATUSES.PENDING:
        self.return_bonus()
        self.return_items()
      if self.status == Order.SHOP_ORDER_STATUSES.CANCELED:
        self.return_bonus()
      if self.status == Order.SHOP_ORDER_STATUSES.PROCEED and self.__original_status == Order.SHOP_ORDER_STATUSES.PENDING:
        self.minus_items()
        self.minus_bonus()
    super(Order, self).save(force_insert, force_update, *args, **kwargs)
    self.__original_status = self.status
    self.__original_payment_status = self.payment_status

  def return_items(self):
    # возращает зарезервированные товары
    items = self.items.all()
    for item in items:
      item.item.count += item.count
      item.item.save()

  def minus_items(self):
    """
     Используется только тогда когда status=PENDING
     то есть мы уже вернули зарезервированные товары
     и теперь нам надо заново их списать
    """
    if self.status == Order.SHOP_ORDER_STATUSES.PENDING:
      items = self.items.all()
      for item in items:
        item.item.count -= item.count
        item.item.save()

  def minus_bonus(self):
    """
     Используется только тогда когда status=PENDING
     то есть мы уже вернули зарезервированные товары
     и теперь нам надо заново их списать
    """
    if self.status == Order.SHOP_ORDER_STATUSES.PENDING:
      self.user.bonus -= self.total_price - self.price_without_bonus
      self.user.save()

  def return_bonus(self):
    """
        Возращаем деньги пользователю
   """
    self.user.bonus += self.total_price - self.price_without_bonus
    self.user.save()

  def has_needed_count(self):
    if self.status == Order.SHOP_ORDER_STATUSES.PENDING:
      items = self.items.all()
      for item in items:
        if item.item.count - item.count < 0:
          return False
      return True
    return True


class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', null=True)
  item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name='orders', verbose_name='Товар')
  count = models.IntegerField(default=1, verbose_name='Количество')
  total_price = models.IntegerField(default=0, verbose_name='Общая сумма')
