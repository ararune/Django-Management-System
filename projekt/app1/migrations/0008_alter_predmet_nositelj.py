# Generated by Django 4.2.2 on 2023-06-09 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_korisnik_uloga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predmet',
            name='nositelj',
            field=models.ForeignKey(limit_choices_to={'uloga__ime': 'professor'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
