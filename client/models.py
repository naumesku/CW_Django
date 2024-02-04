from django.conf import settings
from django.db import models

from config_my import NULLABLE


# Create your models here.

class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              related_name='cleints', related_query_name='client',
                              **NULLABLE, verbose_name='владелец рассылки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'
