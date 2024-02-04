from django.conf import settings
from django.db import models
from client.models import Client
from config_my import NULLABLE
from datetime import date

# Create your models here.
class MailingMessage(models.Model):

    title_message = models.CharField(max_length=50, verbose_name='тема письма')
    body_message = models.TextField(verbose_name='тело письма', **NULLABLE)
    client = models.ManyToManyField(Client, related_name='clients', verbose_name='клиент')
    is_active_mail = models.BooleanField(default=False, verbose_name='активация рассылки')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name="пользователь")

    def __str__(self):
        return '{self.title_message}'

    class Meta:
        verbose_name = 'Сообщение рассылки'
        verbose_name_plural = 'Сообщения рассылок'

class MailingSettings(models.Model):

    class PeriodChoice(models.TextChoices):
        DAILY = 'day', 'раз в день'
        WEEKLY = 'week', 'раз в неделю'
        MONTHLY = 'month', 'раз в месяц'

    class StatusChoice(models.TextChoices):
        CREATED = 'CREATED', 'создана'
        RUNING = 'RUNING', 'запущена'
        ENDET = 'ENDET', 'завершена'

    time = models.TimeField(auto_now_add=True, verbose_name='время создания рассылки')
    period_choices = models.CharField(max_length=50, choices=PeriodChoice.choices,default='day',verbose_name='период рассылки (по умолчанию)')
    status_choices = models.CharField(max_length=50, choices=StatusChoice.choices, default='CREATED', verbose_name='статус рассылки')
    message = models.ForeignKey(MailingMessage, on_delete=models.CASCADE, **NULLABLE, verbose_name='сообщение')
    start_date = models.DateField(default=date.today, verbose_name='начало рассылки (по умолчанию)')
    stop_date = models.DateField(default=date.today, verbose_name='конец рассылки (по умолчанию)')

    def __str__(self):
        return f'{self.time} - {self.message}'

    class Meta:
        verbose_name = 'Настройки рассылки'
        verbose_name_plural = 'Настройки рассылок'


class MailingLogs(models.Model):

    class LogStatus(models.TextChoices):
        GOOD = 'успешно', 'успешно'
        BAD = 'ошибка', 'ошибка'

    date_time = models.DateTimeField(**NULLABLE, verbose_name='дата и время последней рассылки')
    status_try = models.CharField(max_length=25, choices=LogStatus.choices, verbose_name='статус попытки')
    message = models.ForeignKey(MailingMessage, on_delete=models.SET_NULL, **NULLABLE, verbose_name="сообщение")
    answer_server = models.TextField(**NULLABLE, verbose_name='ответ сервера')

    def __str__(self):
        return f'{self.date_time} - {self.status_try}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
