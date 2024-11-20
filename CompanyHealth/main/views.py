from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .forms import LoginForm, RegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            try:
                patient = Patients.objects.get(phone=phone)
                if patient.check_password(password):
                    request.session['patient_id'] = patient.id
                    return redirect('profile')
                else:
                    messages.error(request, 'Неверный пароль.')
            except Patients.DoesNotExist:
                messages.error(request, 'Пользователь с таким номером не найден.')
    else:
        form = LoginForm()

    return render(request, 'main/auth.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Создание нового пользователя
            patient = form.save(commit=False)
            patient.set_password(form.cleaned_data['password'])  # Хэширование пароля
            patient.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти.')
            return redirect('login')  # Перенаправление на страницу входа
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})

def home(request):
    records = Records.objects.all()
    return render(request, 'main/index.html', {'records': records})


def profile_view(request):
    # Получаем текущего пациента, например, по ID из сессии
    patient_id = request.session.get('patient_id')  # предполагаем, что id пациента сохранено в сессии
    if patient_id:
        # Получаем пациента
        patient = Patients.objects.get(id=patient_id)

        # Получаем все записи пациента на прием
        appointments = Appointments.objects.filter(patient=patient)
    else:
        patient = None
        appointments = []

    # Отправляем данные в шаблон
    return render(request, 'main/profile.html', {
        'patient': patient,
        'appointments': appointments
    })