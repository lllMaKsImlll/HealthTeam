from django.db import models

class Patients(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=11)
    email = models.CharField('Почта', max_length=100)

class Doctor(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер', max_length=11)
    email = models.CharField('Почта', max_length=100)
    profession = models.CharField('Специальность', max_length=65)
    experience = models.IntegerField('Стаж')