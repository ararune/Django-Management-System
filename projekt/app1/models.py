# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Uloga(models.Model):
    ime = models.CharField(max_length=13)

    def __str__(self):
        return self.ime

class Korisnik(AbstractUser):
    uloga = models.ForeignKey(Uloga, on_delete=models.CASCADE, null=True)

    STATUS = (
        ('none', 'None'),
        ('redovni', 'Redovni'),
        ('izvanredni', 'Izvanredni'),
    )
    status = models.CharField(max_length=10, choices=STATUS)

    password = models.CharField(max_length=128, default='')


    def __str__(self):
        return self.email

class Predmet(models.Model):
    IZBORNI = (
        ('da', 'Da'),
        ('ne', 'Ne'),
    )

    ime = models.CharField(max_length=255, unique=True)
    kod = models.CharField(max_length=16, unique=True)
    program = models.TextField()
    bodovi = models.IntegerField()
    sem_redovni = models.IntegerField()
    sem_izvanredni = models.IntegerField()
    izborni = models.CharField(max_length=2, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE, limit_choices_to={'uloga__ime': 'professor'})

    def __str__(self):
        return self.ime

class Upis(models.Model):
    STATUS_CHOICES = (
        ('upisan', 'Upisan'),
        ('neupisan', 'Neupisan'),
        ('polozen', 'Položen'),
        ('dobio_potpis', 'Dobio Potpis'),
        ('izgubio_potpis', 'Izgubio Potpis'),
    )

    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmet, on_delete=models.CASCADE)
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, default='upisan', null=True)

    def __str__(self):
        return f"{self.student.email} - {self.predmet.ime}"
