import math
import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from city.models import City

class Shop(models.Model):
  city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='shops', blank=True, null=True,
                           verbose_name='Город')
  address = models.CharField(max_length=300, blank=True, verbose_name='Адрес')
  companyName = models.CharField(max_length=300, blank=True, verbose_name='Название магазина')
  adminPhone = models.CharField(max_length=300, null=True, verbose_name='Номер Админ')
  adminName = models.CharField(max_length=300, null=True, verbose_name='Имя Админа')
  logoUrl = models.FileField(null=True, blank=True)
  admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='shops', blank=True,
                            verbose_name='Админ')

  def __str__(self):
    return "%s %s" % (self.companyName, self.address)

  class Meta:
    verbose_name = 'Магазин'
    verbose_name_plural = 'Магазины'


class ShopWorkTime(models.Model):
  shop = models.OneToOneField(Shop, on_delete=models.CASCADE, related_name='workTime')
  lunch = models.BooleanField(default=False)

  class Meta:
    verbose_name = 'Время работы магазина'


class ShopSchedule(models.Model):
  work_time = models.ForeignKey(ShopWorkTime, related_name='schedule', on_delete=models.CASCADE)
  DAY_NAMES = ((1, 'Понедельник'),
               (2, 'Вторник'),
               (3, 'Среда'),
               (4, 'Четверг'),
               (5, 'Пятница'),
               (6, 'Суббота'),
               (7, 'Воскресенье'))
  day_name = models.IntegerField(choices=DAY_NAMES, default=1)
  first_half_from = models.TimeField(blank=True, null=True)
  first_half_till = models.TimeField(blank=True, null=True)
  second_half_from = models.TimeField(blank=True, null=True)
  second_half_till = models.TimeField(blank=True, null=True)

  class Meta:
    ordering = ['day_name']


class ShopItem(models.Model):
  shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='items')
  name = models.CharField('Название', max_length=300)
  description = models.TextField(verbose_name='Описание')
  sku = models.CharField(max_length=300, verbose_name='Код товара')
  price = models.IntegerField(verbose_name='Цена')
  old_price = models.IntegerField(null=True, blank=True, verbose_name='Старая цена')
  manufacturer = models.CharField(max_length=300, null=True, verbose_name='Производитель')
  count = models.IntegerField(default=0, verbose_name='Количество')
  created_date = models.DateTimeField(verbose_name='Дата создания')
  is_hidden = models.BooleanField(default=False, verbose_name='Скрыть')

  @property
  def discount_percent(self):
    if self.is_sale:
      return 100 - math.ceil(self.price * 100 / self.old_price)
    return None

  @property
  def is_sale(self):
    return self.old_price != None

  @property
  def cover_image(self):
    images = self.images.order_by('is_cover_image').all()
    if images.exists():
      return images[0]
    return None

  def __str__(self):
    return self.name

  class Meta:
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'


class ShopItemImage(models.Model):
  item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name='images')
  image = models.FileField(verbose_name='Фото')
  is_cover_image = models.BooleanField(default=False, verbose_name='Использовать для оболжки')


class ShopItemDetail(models.Model):
  item = models.ForeignKey(ShopItem, on_delete=models.CASCADE, related_name='details')
  name = models.CharField(max_length=300, verbose_name='Название')
  value = models.CharField(max_length=300, verbose_name='Значение')



