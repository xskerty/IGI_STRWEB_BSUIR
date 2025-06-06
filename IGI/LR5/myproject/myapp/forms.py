from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from datetime import date
from .models import (
    UserProfile,
    Patient,
    Doctor,
    Specialization,
    Service,
    Appointment,
    Diagnosis,
    PromoCode,
    Review,
    FAQ,
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Фамилия'
    )
    patronymic = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Отчество'
    )
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[
            RegexValidator(
                regex=r'^\+375\s\(29\)\s\d{3}-\d{2}-\d{2}$',
                message='Введите номер телефона в формате: +375 (29) XXX-XX-XX'
            )
        ],
        label='Телефон'
    )
    role = forms.ChoiceField(
        choices=[('patient', 'Пациент'), ('doctor', 'Врач')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        label='Роль'
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        help_text='Введите дату рождения',
        label='Дата рождения'
    )
    specializations = forms.ModelMultipleChoiceField(
        queryset=Specialization.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label='Специализации'
    )
    education = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Образование'
    )
    experience_years = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        label='Опыт работы (лет)'
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label='Фотография'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'patronymic', 'phone', 'role', 'date_of_birth', 'specializations', 'education', 'experience_years', 'photo', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }
        help_texts = {
            'username': 'Обязательное поле. 150 символов или меньше. Только буквы, цифры и символы @/./+/-/_',
            'password1': 'Ваш пароль должен содержать как минимум 8 символов и не может быть полностью числовым.',
            'password2': 'Введите тот же пароль, что и выше, для подтверждения.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем подсказки для полей
        self.fields['username'].help_text = 'Обязательное поле. 150 символов или меньше. Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = 'Пароль должен содержать минимум 8 символов'
        self.fields['password2'].help_text = 'Введите тот же пароль для подтверждения'

        # Добавляем JavaScript для динамического отображения полей врача
        self.fields['role'].widget.attrs['onchange'] = '''
            var role = document.querySelector('input[name="role"]:checked').value;
            var doctorFields = document.getElementById('doctor-fields');
            if (role === 'doctor') {
                doctorFields.style.display = 'block';
            } else {
                doctorFields.style.display = 'none';
            }
        '''

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise forms.ValidationError('Вы должны быть старше 18 лет для регистрации')
        return dob

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        education = cleaned_data.get('education')
        experience_years = cleaned_data.get('experience_years')
        specializations = cleaned_data.get('specializations')
        photo = cleaned_data.get('photo')

        if role == 'doctor':
            if not education:
                self.add_error('education', 'Это поле обязательно для врачей')
            if experience_years is None:
                self.add_error('experience_years', 'Это поле обязательно для врачей')
            if not specializations:
                self.add_error('specializations', 'Выберите хотя бы одну специализацию')
            if not photo:
                self.add_error('photo', 'Загрузите фотографию')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Создаем профиль пользователя с отчеством
            UserProfile.objects.create(
                user=user,
                middle_name=self.cleaned_data.get('patronymic', '')
            )
        return user

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['phone', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['phone', 'specializations', 'experience_years', 'education', 'photo', 'date_of_birth']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'specializations': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }

class SpecializationForm(forms.ModelForm):
    class Meta:
        model = Specialization
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'duration_minutes', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.doctor = kwargs.pop('doctor', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.doctor:
            instance.doctor = self.doctor
        if commit:
            instance.save()
        return instance

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'service', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doctor'].queryset = Doctor.objects.filter(is_active=True)

class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['patient', 'name', 'description', 'date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class PromocodeForm(forms.ModelForm):
    class Meta:
        model = PromoCode
        fields = ['code', 'discount']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['doctor', 'rating', 'text', 'review_date']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5}),
            'review_date': forms.DateInput(attrs={'type': 'date'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not kwargs.get('instance') and not kwargs.get('initial', {}).get('is_superuser'):
            self.fields.pop('category', None)
            self.fields.pop('status', None)
