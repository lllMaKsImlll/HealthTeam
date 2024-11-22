from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.utils import timezone

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            try:
                patient = Patient.objects.get(phone=phone)
                if patient.check_password(password):
                    request.session['patient_id'] = patient.id
                    return redirect('profile')
                else:
                    messages.error(request, 'Неверный пароль.')
            except Patient.DoesNotExist:
                messages.error(request, 'Пользователь с таким номером не найден.')
    else:
        form = LoginForm()

    return render(request, 'main/auth.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.set_password(form.cleaned_data['password'])
            patient.save()
            return redirect('login')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})


def home(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    records = Record.objects.all()
    records = Record.objects.all()
    return render(request, 'main/index.html', {
        'records': records,
        'patient': patient,
    })


@login_required
def profile_view(request):
    # Получаем идентификатор пациента из сессии
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return render(request, 'main/profile.html', {'error': 'Пациент не найден.'})

    # Получаем пациента по ID
    patient = get_object_or_404(Patient, id=patient_id)

    # Получаем все записи на прием для пациента
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'main/profile.html', {
        'patient': patient,
        'appointments': appointments
    })

def logout_view(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
    return redirect('index')


def appointments_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    search_results = None  # Результаты поиска
    profession = ''
    area = ''

    if request.method == "POST":
        # Получаем данные из формы.
        profession = request.POST.get('profession', '').strip()
        area = request.POST.get('district', '').strip()

        # Выполняем поиск по специальности и району, если они указаны.
        query = Doctor.objects.all()
        if profession:
            query = query.filter(profession__icontains=profession)
        if area:
            query = query.filter(area__icontains=area)

        # Если запрос ничего не нашел, передаём пустой список.
        search_results = query if query.exists() else []

    return render(request, 'main/appointments.html', {
        'search_results': search_results,
        'profession': profession,  # Передаём введённую специальность
        'district': area,  # Передаём введённый район
        'patient': patient,
    })

def contacts_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    return render(request, 'main/contacts.html', {
        'patient': patient,
    })

def aboutUs_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/aboutUs.html',{
        'patient': patient,
    })

def ourServices_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/ourServices.html', {
        'patient': patient,
    })

def news_view(request):
    news_list = News.objects.all().order_by('-date')
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/news.html', {
        'patient': patient,
        'news_list': news_list
    })


def questions_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/questions.html', {
        'patient': patient,
    })

def editProfile_view(request):
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/editProfile.html', {
        'patient': patient,
    })

def make_appointment(request, doctor_id):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')

        if appointment_date:
            try:
                appointment_date = timezone.datetime.strptime(appointment_date,"%Y-%m-%dT%H:%M")  # Обратите внимание на формат
            except ValueError:
                return render(request, 'main/make_appointment.html', {
                    'doctor': doctor,
                    'error': 'Неверный формат даты и времени.'
                })

            appointment_description = request.POST.get('description', '')

            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                date=appointment_date,
                description=appointment_description
            )

            return redirect('profile')  # Перенаправляем на профиль после записи

        else:
            return render(request, 'main/make_appointment.html', {
                'doctor': doctor,
                'error': 'Дата и время приема не могут быть пустыми.'
            })

    return render(request, 'main/make_appointment.html', {'doctor': doctor})