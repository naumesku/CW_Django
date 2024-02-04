# Generated by Django 4.2.7 on 2024-01-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0004_mailingmessage_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailingsettings',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='конец рассылки'),
        ),
        migrations.AddField(
            model_name='mailingsettings',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='начало рассылки'),
        ),
    ]
