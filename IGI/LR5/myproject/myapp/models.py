from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
import pytz
from PIL import Image
import os

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    middle_name = models.CharField(max_length=150, blank=True, verbose_name='Отчество')

    def __str__(self):
        return f"{self.user.get_full_name()} {self.middle_name}"

    def get_full_name(self):
        full_name = f"{self.user.last_name} {self.user.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return full_name.strip()

    def get_short_name(self):
        short_name = f"{self.user.last_name} {self.user.first_name[0]}."
        if self.middle_name:
            short_name += f"{self.middle_name[0]}."
        return short_name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.profile.get_full_name()}"

def doctor_photo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'doctor_photos/doctor_{instance.id}.{ext}'
    return filename

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    specializations = models.ManyToManyField('Specialization', related_name='doctors')
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True)
    photo = models.ImageField(upload_to=doctor_photo_path, null=True, blank=True)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {', '.join(str(spec) for spec in self.specializations.all())}"

    def save(self, *args, **kwargs):
        if self.photo:
            img = Image.open(self.photo)
            
            if img.width > 400 or img.height > 400:
                output_size = (400, 400)
                img.thumbnail(output_size)
                
                # Сохраняем изображение
                img.save(self.photo.path, quality=95, optimize=True)
        
        super().save(*args, **kwargs)

class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='services', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment {self.id} - {self.patient} with Dr. {self.doctor}"

    class Meta:
        ordering = ['appointment_date']

class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='diagnoses')
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.patient}"

class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reviews')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    text = models.TextField()
    review_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Отзыв от {self.patient.user.get_full_name()} для {self.doctor.user.get_full_name()}'

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    short_content = models.CharField(max_length=200)
    image = models.ImageField(upload_to='articles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class CompanyInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_url = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to='company/', null=True, blank=True)
    requisites = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class CompanyHistory(models.Model):
    year = models.IntegerField()
    description = models.TextField()
    company_info = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='history')

    class Meta:
        ordering = ['year']
        verbose_name_plural = 'Company history'

    def __str__(self):
        return f"{self.year} - {self.description[:50]}"

class News(models.Model):
    title = models.CharField(max_length=200)
    short_content = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faq_questions')
    answer_author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='faq_answers')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

class Contact(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='contacts/')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.position}"

class Vacancy(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.code

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            (self.start_date is None or self.start_date <= now) and
            (self.end_date is None or self.end_date >= now)
        )