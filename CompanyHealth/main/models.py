from django.db import models

class Patients(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=11)
    email = models.CharField('Почта', max_length=100)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.fio

class Doctor(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер', max_length=11)
    email = models.CharField('Почта', max_length=100)
    profession = models.CharField('Специальность', max_length=65)
    experience = models.IntegerField('Стаж')
    image = models.ImageField('Изображение',null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.fio

class Records(models.Model):
    name = models.CharField('Имя', max_length=35)
    record = models.TextField('Отзыв')
    date = models.CharField('Дата отзыва', max_length=25)
    image = models.ImageField('Изображение', null=True, blank=True, upload_to='images/')
    def __str__(self):
        return f"{self.name} {self.date}"