from django.db import models


class City(models.Model):
  name = models.CharField(max_length=200, null=True)

  def __str__(self):
    return "%s" % (self.name)

  class Meta:
    verbose_name = 'Город'
    verbose_name_plural = 'Города'

