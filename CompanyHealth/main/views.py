from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required

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
    return render(request, 'main/index.html', {
        'records': records,
        'patient': patient,
    })


def profile_view(request):
    patient_id = request.session.get('patient_id')
    if patient_id:
        patient = Patient.objects.get(id=patient_id)
        appointments = Appointment.objects.filter(patient=patient)
    else:
        patient = None
        appointments = []

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
    patient_id = request.session.get('patient_id')
    patient = None
    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None
    return render(request, 'main/news.html', {
        'patient': patient,
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

# Hello world