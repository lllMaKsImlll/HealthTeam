from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Patient(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=11)
    email = models.CharField('Почта', max_length=100)
    image = models.ImageField('Изображение профиля', null=True, blank=True, upload_to='images/')
    password = models.CharField('Пароль', max_length=120)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.fio


class Doctor(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер', max_length=11)
    email = models.CharField('Почта', max_length=100)
    profession = models.CharField('Специальность', max_length=65)
    experience = models.IntegerField('Стаж')
    room = models.CharField('Кабинет', max_length=50)
    area = models.CharField('Район работы', max_length=100)
    adress = models.CharField('Адрес кабинета', max_length=120)
    image = models.ImageField('Изображение профиля', null=True, blank=True, upload_to='images/')
    password = models.CharField('Пароль', max_length=120)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.fio


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name='Пациент')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name='Врач')
    date = models.DateTimeField('Дата и время приема')
    description = models.TextField('Описание проблемы', blank=True, null=True)
    recommendations = models.TextField('Рекомендации', blank=True, null=True)
    visited = models.BooleanField('Посещенно', default=False)

    def __str__(self):
        return f"Прием {self.patient.fio} у {self.doctor.fio}"

class Record(models.Model):
    name = models.CharField('Имя', max_length=35)
    record = models.TextField('Отзыв')
    date = models.CharField('Дата отзыва', max_length=25)
    image = models.ImageField('Изображение профиля', null=True, blank=True, upload_to='images/')
    def __str__(self):
        return f"{self.name} {self.date}"

class News(models.Model):
    title = models.CharField('Заголовок', max_length=60)
    text = models.TextField('Описание новости')
    date = models.CharField('Дата выпуска новости', max_length=30)

    def __str__(self):
        return f" новость {self.title} от {self.date}"