# Generated by Django 4.2.7 on 2024-02-03 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0002_client_owner'),
        ('mailing', '0006_alter_mailingmessage_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingmessage',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mails', related_query_name='mail', to=settings.AUTH_USER_MODEL, verbose_name='автор рассылки'),
        ),
        migrations.AlterField(
            model_name='mailingmessage',
            name='client',
            field=models.ManyToManyField(related_name='clients', to='client.client', verbose_name='клиент'),
        ),
    ]