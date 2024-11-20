from django import forms
from django.core.exceptions import ValidationError
from .models import *

class LoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        label=None,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'})
    )
    password = forms.CharField(
        label=None,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )

    confirm_password = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
    )

    class Meta:
        model = Patients
        fields = ['fio', 'phone', 'email', 'password']
        widgets = {
            'fio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите почту'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Patients.objects.filter(phone=phone).exists():
            raise ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Patients.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError('Пароли не совпадают.')
        return cleaned_data