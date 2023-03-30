from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class MediaFile(models.Model):
    file = models.FileField()


class Version(models.Model):
    class TYPES:
        FLUTTER = 'flutter'
        IOS = 'ios'
        ANDROID = 'android'
        TYPE_CHOICES = [(FLUTTER, 'Flutter'), (IOS, 'ios'), (ANDROID, 'android')]

    type = models.CharField(choices=TYPES.TYPE_CHOICES, unique=True, max_length=150)
    version = models.CharField(max_length=120)
    hard = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Версия приложения'
        verbose_name_plural = 'Версия приложения'


class ResponseAboutApp(models.Model):
    class STATUES:
        PROCESSED = 0
        IN_PROCESS = 1
        DONE = 2

        STATUS_CHOICES = [(PROCESSED, 'В обработке'), (IN_PROCESS, 'В пути'),
                          (DONE, 'Завершено')]

    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True,
                             related_name='response_about_app', verbose_name='Пользователь')
    message = models.TextField('Отзыв')
    status = models.IntegerField('Статус', choices=STATUES.STATUS_CHOICES, default=STATUES.PROCESSED)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Последнее изменение', auto_now=True)

    class Meta:
        verbose_name = 'Отзыв о приложении'
        verbose_name_plural = 'Отзывы о приложении'
