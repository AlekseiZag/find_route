# Generated by Django 3.1.3 on 2021-05-23 21:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Имя пользователя'),
        ),
    ]
