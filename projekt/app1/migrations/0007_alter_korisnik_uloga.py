# Generated by Django 4.2.2 on 2023-06-06 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_korisnik_password_alter_korisnik_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='korisnik',
            name='uloga',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.uloga'),
        ),
    ]