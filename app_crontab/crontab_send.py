from mailing.models import MailingMessage, MailingSettings
from mailing.utils import send_mailing, actually_status_mailing


def mailings_day():
    actually_status_mailing()
    mailings_all_dayly = MailingMessage.objects.filter(is_active_mail=True,
                                                       mailingsettings__status_choices=MailingSettings.StatusChoice.RUNING,
                                                       mailingsettings__period_choices=MailingSettings.PeriodChoice.DAILY,
                                                       )
    print(f'mailings_all_dayly = {mailings_all_dayly}')
    send_mailing(mailings_all_dayly)

def mailings_week():
    actually_status_mailing()
    mailings_all_week = MailingMessage.objects.filter(is_active_mail=True,
                                                       mailingsettings__status_choices=MailingSettings.StatusChoice.RUNING,
                                                       mailingsettings__period_choices=MailingSettings.PeriodChoice.WEEKLY,
                                                       )
    send_mailing(mailings_all_week)


def mailings_month():
    actually_status_mailing()
    mailings_all_month = MailingMessage.objects.filter(is_active_mail=True,
                                                       mailingsettings__status_choices=MailingSettings.StatusChoice.RUNING,
                                                       mailingsettings__period_choices=MailingSettings.PeriodChoice.MONTHLY,
                                                       )
    send_mailing(mailings_all_month)
