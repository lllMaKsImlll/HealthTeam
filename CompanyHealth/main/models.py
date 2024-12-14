from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

class Patient(models.Model):
    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=11)
    email = models.CharField('Почта', max_length=100)
    image = models.ImageField('Изображение профиля', null=True, blank=True, upload_to='images/')
    password = models.CharField('Пароль', max_length=120)
    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"

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
    GENDER_CHOICES = [
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
    ]

    PROFESSION_CHOICES = [
        ("Терапевт", "Терапевт"),
        ("Хирург", "Хирург"),
        ("Педиатр", "Педиатр"),
        ("Офтальмолог", "Офтальмолог"),
        ("Кардиолог", "Кардиолог"),
        ("Невролог", "Невролог"),
        ("Эндокринолог", "Эндокринолог"),
        ("Дерматолог", "Дерматолог"),
        ("Уролог", "Уролог"),
        ("Гинеколог", "Гинеколог"),
        ("Отоларинголог (ЛОР)", "Отоларинголог (ЛОР)"),
        ("Стоматолог", "Стоматолог"),
        ("Психиатр", "Психиатр"),
        ("Пульмонолог", "Пульмонолог"),
        ("Гастроэнтеролог", "Гастроэнтеролог"),
        ("Ревматолог", "Ревматолог"),
        ("Онколог", "Онколог"),
        ("Травматолог-ортопед", "Травматолог-ортопед"),
        ("Фтизиатр", "Фтизиатр"),
        ("Инфекционист", "Инфекционист"),
        ("Нефролог", "Нефролог"),
        ("Гематолог", "Гематолог"),
        ("Аллерголог-иммунолог", "Аллерголог-иммунолог"),
        ("Венеролог", "Венеролог"),
        ("Сосудистый хирург", "Сосудистый хирург"),
        ("Ангиолог", "Ангиолог"),
        ("Анестезиолог-реаниматолог", "Анестезиолог-реаниматолог"),
        ("Маммолог", "Маммолог"),
        ("Проктолог", "Проктолог"),
        ("Гепатолог", "Гепатолог"),
        ("Косметолог", "Косметолог"),
        ("Физиотерапевт", "Физиотерапевт"),
        ("Логопед", "Логопед"),
        ("Дефектолог", "Дефектолог"),
        ("Генетик", "Генетик"),
    ]

    DISTRICT_CHOICES = [
        ("Центральный", "Центральный"),
        ("Калининский", "Калининский"),
        ("Курчатовский", "Курчатовский"),
        ("Ленинский", "Ленинский"),
        ("Металлургический", "Металлургический"),
        ("Советский", "Советский"),
        ("Тракторозаводский", "Тракторозаводский"),
    ]

    fio = models.CharField('ФИО', max_length=100)
    phone = models.CharField('Номер телефона', max_length=11)
    email = models.CharField('Почта', max_length=100)
    profession = models.CharField('Специальность', max_length=65, choices=PROFESSION_CHOICES)
    experience = models.IntegerField('Стаж')
    room = models.CharField('Кабинет', max_length=50)
    area = models.CharField('Район работы', max_length=100, choices=DISTRICT_CHOICES)
    adress = models.CharField('Адрес кабинета', max_length=120)
    image = models.ImageField('Изображение профиля', blank=True, upload_to='images/')
    password = models.CharField('Пароль', max_length=120)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, default='M')

    class Meta:
        verbose_name = "Доктор"
        verbose_name_plural = "Доктора"

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

    class Meta:
        verbose_name = "Запись на прием"
        verbose_name_plural = "Записи на прием"

    def __str__(self):
        return f"Прием {self.patient.fio} у {self.doctor.fio}"

class Record(models.Model):
    name = models.CharField('Имя', max_length=35)
    record = models.TextField('Отзыв')
    date = models.CharField('Дата отзыва', max_length=25)
    image = models.ImageField('Изображение профиля', null=True, blank=True, upload_to='images/')

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    def __str__(self):
        return f"{self.name} {self.date}"



class News(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Описание новости')
    date = models.CharField('Дата выпуска новости', max_length=30)
    image = models.ImageField('Изображение для новости', null=True, blank=True, upload_to='images/')

    class Meta:
        verbose_name = "Новости"
        verbose_name_plural = "Новости"

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.now().strftime('%d.%m.%Y')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"новость {self.title} от {self.date}"



class HomeVisit(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'В ожидании'),
        ('ASSIGNED', 'Назначен врач'),
        ('COMPLETED', 'Завершено'),
        ('CANCELLED', 'Отменено'),
    ]

    patient_name = models.CharField('Имя пациента', max_length=255)
    patient_phone = models.CharField('Контактный телефон', max_length=15)
    address = models.CharField('Адрес вызова', max_length=100)
    symptoms = models.TextField('Симптомы', blank=True, null=True)
    requested_time = models.DateTimeField('Время запроса', auto_now_add=True)
    scheduled_time = models.DateTimeField('Запланированное время визита', null=True, blank=True)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_visits', verbose_name='Назначенный врач')
    status = models.CharField('Статус', max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        verbose_name = 'Вызов врача на дом'
        verbose_name_plural = 'Вызовы врачей на дом'
        ordering = ['-requested_time']

    def __str__(self):
        return f"Вызов {self.patient_name} на {self.address} ({self.get_status_display()})"


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="schedules", verbose_name="Врач")
    date = models.DateField("Дата рабочего дня")
    start_time = models.TimeField("Время начала работы", default="08:00")
    end_time = models.TimeField("Время окончания работы", default="20:00")
    break_start = models.TimeField("Начало перерыва", blank=True, default="13:00")
    break_end = models.TimeField("Конец перерыва", blank=True, default="14:00")

    class Meta:
        verbose_name = "Расписание врача"
        verbose_name_plural = "Расписания врачей"

    def __str__(self):
        return f"{self.doctor.fio} - {self.date}"

class Question(models.Model):
    email = models.EmailField("Email пациента")
    question_text = models.TextField("Вопрос")
    created_at = models.DateTimeField("Дата и время создания", auto_now_add=True)

    def __str__(self):
        return f"Вопрос {self.created_at}"

    class Meta:
        verbose_name = "Вопросы пациентов"
        verbose_name_plural = "Вопросы пациентов"