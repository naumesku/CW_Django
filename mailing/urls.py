from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.apps import MailingConfig
from mailing.views import MailingMessageListView, MailingMessageCreateView, MailingMessageDetailView, \
    MailingMessageUpdateView, MailingMessageDeleteView, toggle_activity, main_page, mailing_logs

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingMessageListView.as_view(), name='index'),
    path('create/', MailingMessageCreateView.as_view(), name='create'),
    path('view/<int:pk>/', MailingMessageDetailView.as_view(), name='view'),
    path('mailing_update/<int:pk>/', MailingMessageUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingMessageDeleteView.as_view(), name='mailing_delete'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity'),
    path('main_page/', main_page, name='main_page'),
    path('logs/', mailing_logs, name='logs'),

]
