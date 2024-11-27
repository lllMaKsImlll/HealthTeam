from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.http import HttpResponseForbidden
from django.utils import timezone


def login_view(request):
    next_url = request.GET.get('next', 'profile')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            patient = Patient.objects.filter(phone=phone).first()
            if patient and patient.check_password(password):
                # Устанавливаем сессию для пациента
                request.session['user_type'] = 'patient'
                request.session['patient_id'] = patient.id
                return redirect(next_url)

            doctor = Doctor.objects.filter(phone=phone).first()
            if doctor and doctor.check_password(password):
                # Устанавливаем сессию для доктора
                request.session['user_type'] = 'doctor'
                request.session['doctor_id'] = doctor.id
                return redirect(next_url)

            messages.error(request, 'Неверный номер телефона или пароль.')
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
    professions = ['Терапевт', 'Хирург', 'Педиатр', 'Офтальмолог']
    districts = ['Центральный', 'Ленинский', 'Советский', 'Калининский']

    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

    records = Record.objects.all()

    return render(request, 'main/index.html', {
        'records': records,
        'patient': patient,
        'doctor': doctor,  # Передаем данные доктора
        'professions': professions,
        'districts': districts
    })


@login_required
def profile_view(request):
    user_type = request.session.get('user_type')
    professions = ['Терапевт', 'Хирург', 'Педиатр', 'Офтальмолог']

    if user_type == 'patient':
        patient_id = request.session.get('patient_id')
        if not patient_id:
            return render(request, 'main/profilePacient.html', {'error': 'Пациент не найден.'})

        patient = get_object_or_404(Patient, id=patient_id)

        upcoming_appointments = Appointment.objects.filter(patient=patient).exclude(visited=True)
        visited_appointments = Appointment.objects.filter(patient=patient, visited=True)

        filter_specialty = request.GET.get('specialty', '').strip()
        filter_date = request.GET.get('date', '').strip()

        if filter_specialty:
            upcoming_appointments = upcoming_appointments.filter(doctor__profession__icontains=filter_specialty)
        if filter_date:
            upcoming_appointments = upcoming_appointments.filter(date__date=filter_date)

        return render(request, 'main/profilePacient.html', {
            'patient': patient,
            'professions': professions,
            'upcoming_appointments': upcoming_appointments,
            'visited_appointments': visited_appointments,
            'filter_specialty': filter_specialty,
            'filter_date': filter_date,
        })

    elif user_type == 'doctor':
        doctor_id = request.session.get('doctor_id')
        if not doctor_id:
            return render(request, 'main/profileDoctor.html', {'error': 'Доктор не найден.'})

        doctor = get_object_or_404(Doctor, id=doctor_id)
        upcoming_appointments = Appointment.objects.filter(doctor=doctor).exclude(visited=True)
        visited_appointments = Appointment.objects.filter(doctor=doctor, visited=True)

        filter_date = request.GET.get('date', '').strip()

        if filter_date:
            upcoming_appointments = upcoming_appointments.filter(date__date=filter_date)

        return render(request, 'main/profileDoctor.html', {
            'doctor': doctor,
            'professions': professions,
            'upcoming_appointments': upcoming_appointments,  # Приводим название к тому, что используется в шаблоне
            'visited_appointments': visited_appointments,
            'filter_date': filter_date,
        })

    return redirect('login')

def logout_view(request):
    if 'patient_id' in request.session:
        del request.session['patient_id']
    if 'doctor_id' in request.session:
        del request.session['doctor_id']
    return redirect('index')


def appointments_view(request):
    professions = ['Терапевт', 'Хирург', 'Педиатр', 'Офтальмолог']
    districts = ['Центральный', 'Ленинский', 'Советский', 'Калининский']
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

    search_results = None
    profession = ''
    area = ''

    if profession == '' and area == '':
        search_results = Doctor.objects.all()

    if request.method == "POST":
        profession = request.POST.get('profession', '').strip()
        area = request.POST.get('district', '').strip()

        query = Doctor.objects.all()
        if profession:
            query = query.filter(profession__icontains=profession)
        if area:
            query = query.filter(area__icontains=area)

        search_results = query if query.exists() else []

    return render(request, 'main/appointments.html', {
        'search_results': search_results,
        'profession': profession,
        'district': area,
        'patient': patient,
        'doctor': doctor,
        'professions': professions,
        'districts': districts
    })

def contacts_view(request):
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

    return render(request, 'main/contacts.html', {
        'patient': patient,
        'doctor': doctor,
    })

def aboutUs_view(request):
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None


    return render(request, 'main/aboutUs.html',{
        'patient': patient,
        'doctor': doctor,
    })

def ourServices_view(request):
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

    return render(request, 'main/ourServices.html', {
        'patient': patient,
        'doctor': doctor,
    })

def news_view(request):
    news_list = News.objects.all().order_by('-date')
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None


    return render(request, 'main/news.html', {
        'patient': patient,
        'doctor': doctor,
        'news_list': news_list
    })


def questions_view(request):
    patient_id = request.session.get('patient_id')
    doctor_id = request.session.get('doctor_id')

    patient = None
    doctor = None

    if patient_id:
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            patient = None

    if doctor_id:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
        except Doctor.DoesNotExist:
            doctor = None

    return render(request, 'main/questions.html', {
        'patient': patient,
        'doctor': doctor,
    })


def editProfile_view(request):
    patient_id = request.session.get('patient_id')
    if not patient_id:
        return redirect('login')

    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        if 'remove_image' in request.POST:
            if patient.image:
                patient.image.delete()  # Удаляем файл изображения
                patient.image = None
                patient.save()
                messages.success(request, "Изображение профиля удалено.")
            return redirect('editProfile')

        fio = request.POST.get('fio')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')

        if fio:
            patient.fio = fio
        if email:
            patient.email = email
        if phone:
            patient.phone = phone
        if image:
            patient.image = image

        if old_password and new_password and confirm_password:
            if new_password != confirm_password:
                messages.error(request, "Новые пароли не совпадают.")
            elif not patient.user.check_password(old_password):
                messages.error(request, "Старый пароль указан неверно.")
            else:
                patient.user.set_password(new_password)
                patient.user.save()
                messages.success(request, "Пароль успешно изменен.")

        patient.save()
        messages.success(request, "Данные профиля успешно обновлены.")
        return redirect('profile')

    return render(request, 'main/editProfile.html', {
        'patient': patient,
    })


def make_appointment(request, doctor_id):
    if request.method == "POST":
        patient_id = request.session.get('patient_id')
        #doctor_id = request.session.get('doctor_id')

        #if doctor_id:
        #    return HttpResponseForbidden("Врачу нельзя записываться на приемы, только пациентам")

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return redirect('login')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        appointment_date = request.POST.get('appointment_date')
        description = request.POST.get('description', '').strip()

        if not appointment_date:
            return render(request, 'main/make_appointment.html', {
                'doctor': doctor,
                'error_message': 'Дата и время приема обязательны.'
            })

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=appointment_date,
            description=description
        )
        return redirect('profile')

    doctor = get_object_or_404(Doctor, id=doctor_id)
    return render(request, 'main/make_appointment.html', {'doctor': doctor})

@login_required
def cancel_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if appointment.patient.id != request.session.get('patient_id'):
            return redirect('profile')

        appointment.delete()
        return redirect('profile')

    messages.error(request, 'Неверный метод запроса.')
    return redirect('profile')


def specific_appointment_for_patient(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    patient = appointment.patient
    doctor = appointment.doctor

    if request.method == 'POST':
        recommendations = request.POST.get('recommendations', '').strip()
        visited = request.POST.get('visited') == 'on'

        appointment.recommendations = recommendations
        appointment.visited = visited
        appointment.save()

        return redirect('profile')

    return render(request, 'main/specificAppointmentForPacient.html', {
        'appointment': appointment,
        'patient': patient,
        'doctor': doctor
    })


def specific_appointment_for_doctor(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    patient = appointment.patient
    doctor = appointment.doctor

    return render(request, 'main/specificAppointmentForDoctor.html', {
        'appointment': appointment,
        'patient': patient,
        'doctor': doctor
    })

def create_home_visit(request):
    if request.method == 'POST':
        patient_name = request.POST['patient_name']
        patient_phone = request.POST['patient_phone']
        address = request.POST['address']
        symptoms = request.POST.get('symptoms', '')

        # Сохранение вызова
        HomeVisit.objects.create(
            patient_name=patient_name,
            patient_phone=patient_phone,
            address=address,
            symptoms=symptoms
        )
        return redirect('home_visits_list')  # Переход на страницу со списком вызовов

    return render(request, 'main/create_home_visit.html')


from django.shortcuts import render
from .models import HomeVisit


def home_visits_list(request):
    status_filter = request.GET.get('status', 'PENDING')

    if status_filter == 'PENDING':
        visits = HomeVisit.objects.filter(status='PENDING')
    elif status_filter == 'ASSIGNED':
        visits = HomeVisit.objects.filter(status='ASSIGNED')
    elif status_filter == 'COMPLETED':
        visits = HomeVisit.objects.filter(status='COMPLETED')
    elif status_filter == 'CANCELLED':
        visits = HomeVisit.objects.filter(status='CANCELLED')
    else:
        visits = HomeVisit.objects.all()

    return render(request, 'main/home_visits_list.html', {
        'visits': visits,
        'status_filter': status_filter,
    })


@login_required
def doctor_appointments(request):
    doctor_id = request.user.id  # или если есть идентификатор врача, который связан с пользователем
    appointments = Appointment.objects.filter(doctor_id=doctor_id, visited=False).order_by('date')
    home_visits = HomeVisit.objects.filter(doctor_id=doctor_id, status='ASSIGNED').order_by('scheduled_time')

    return render(request, 'main/doctor_appointments.html', {
        'appointments': appointments,
        'home_visits': home_visits,
    })
