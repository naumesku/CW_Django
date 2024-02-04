from django.contrib import admin
from .models import MailingSettings, MailingMessage


class MailingSettingsInline(admin.StackedInline):
    model = MailingSettings
    extra = 1
    can_delete = False
    verbose_name = 'настройки рассылки'
    verbose_name_plural = 'настройки рассылок'


@admin.register(MailingMessage)
class MailingMessage(admin.ModelAdmin):
    list_display = ('title_message', 'owner',)
    list_filter = ('owner',)
    inlines = [
        MailingSettingsInline,
    ]