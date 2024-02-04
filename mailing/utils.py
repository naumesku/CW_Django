import smtplib

from django.conf import settings
from django.core.mail import send_mail
from mailing.models import MailingMessage, MailingSettings, MailingLogs
from datetime import datetime, date

def actually_status_mailing():
    today = date.today()

    mailing_create = MailingMessage.objects.filter(
        is_active_mail=True,
        mailingsettings__status_choices=MailingSettings.StatusChoice.CREATED,
        mailingsettings__start_date__lte=today,
        mailingsettings__stop_date__gte=today,

    )

    if mailing_create.exists():
        for mail in mailing_create:
            for mailing in mail.mailingsettings_set.filter(message_id=mail.pk):
                mailing.status_choices = MailingSettings.StatusChoice.RUNING
                mailing.save()

    mailing_end = MailingSettings.objects.filter(
        status_choices=MailingSettings.StatusChoice.RUNING,
        stop_date__lt=today,
    )

    if mailing_end.exists():
        for mail_end in mailing_end:
            for mailing in mail_end.mailingsettings_set.filter(message_id=mail_end.pk):
                mailing.status_choices = MailingSettings.StatusChoice.ENDET
                mailing.save()

def send_mailing(mailings_all):

    for message in mailings_all:
         try:
            recipient_list = message.client.all()

            send_mail(
                subject=message.title_message,
                message=message.body_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
            )
         except smtplib.SMTPException as error:
             MailingLogs.objects.create(
                 date_time=datetime.now(),
                 status_try=MailingLogs.LogStatus.BAD,
                 message=message,
                 answer_server=error,
             )
         MailingLogs.objects.create(
             date_time=datetime.now(),
             status_try=MailingLogs.LogStatus.GOOD,
             message=message,
             answer_server='Ок',
         )


