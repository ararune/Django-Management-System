# Generated by Django 4.2.2 on 2023-06-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='korisnik',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='korisnik',
            name='password',
            field=models.CharField(default='1234', max_length=128),
        ),
        migrations.AlterField(
            model_name='korisnik',
            name='email',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
