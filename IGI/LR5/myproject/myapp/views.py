import matplotlib
matplotlib.use('Agg')  # Используем бэкенд без GUI
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.db.models import Sum, Count, Avg, ExpressionWrapper, F, FloatField, Min, Max
from django.db.models.functions import TruncMonth
from django.utils import timezone as dj_timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import (
    Patient,
    Doctor,
    Specialization,
    Service,
    Appointment,
    Diagnosis,
    Review,
    Article,
    CompanyInfo,
    News,
    FAQ,
    Contact,
    PromoCode,
    Vacancy
)
from .forms import (
    UserRegistrationForm,
    PatientProfileForm,
    DoctorProfileForm,
    ServiceForm,
    AppointmentForm,
    DiagnosisForm,
    ReviewForm,
    PromocodeForm,
    FAQForm
)
from statistics import median, mode
from django.utils.decorators import method_decorator
import requests
from django.views.generic import View
import io
import base64
from django.db.models.functions import Coalesce
import calendar

def is_doctor(user):
    return hasattr(user, 'doctor_profile')

def is_patient(user):
    return hasattr(user, 'patient_profile')

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = datetime.now()
        year = today.year
        month = today.month
        
        cal = calendar.monthcalendar(year, month)
        
        days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        
        month_name = calendar.month_name[month]
        
        context['calendar'] = {
            'days_of_week': days_of_week,
            'month_name': month_name,
            'year': year,
            'weeks': cal,
            'today': today.day
        }
        
        context['latest_news'] = News.objects.order_by('-created_at').first()
        
        try:
            resp = requests.get('https://api.open-meteo.com/v1/forecast?latitude=53.9&longitude=27.5667&current_weather=true', timeout=5)
            data = resp.json()
            context['weather'] = data['current_weather']
        except Exception as e:
            context['weather'] = None
            context['weather_error'] = str(e)


        try:
            resp = requests.get('https://catfact.ninja/fact', timeout=5)
            data = resp.json()
            if 'fact' in data:
                context['cat_fact'] = data['fact']
            else:
                context['cat_fact'] = None
        except Exception as e:
            context['cat_fact'] = None
            context['cat_fact_error'] = str(e)

        return context

class ServiceListView(ListView):
    model = Service
    template_name = 'services.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = Service.objects.all()
        
        # Фильтр по цене
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        # Сортировка
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'popular':
            queryset = queryset.annotate(
                appointment_count=Count('appointments')
            ).order_by('-appointment_count')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем минимальную и максимальную цены для фильтров
        min_price = Service.objects.aggregate(Min('price'))['price__min']
        max_price = Service.objects.aggregate(Max('price'))['price__max']
        
        context.update({
            'min_price': min_price,
            'max_price': max_price,
            'current_min_price': self.request.GET.get('min_price', min_price),
            'current_max_price': self.request.GET.get('max_price', max_price),
            'current_sort': self.request.GET.get('sort', ''),
        })
        
        return context

class AppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        if hasattr(self.request.user, 'doctor_profile'):
            return Appointment.objects.filter(doctor=self.request.user.doctor_profile)
        elif hasattr(self.request.user, 'patient_profile'):
            return Appointment.objects.filter(patient=self.request.user.patient_profile)
        return Appointment.objects.none()

class AppointmentCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointments')

    def test_func(self):
        return is_patient(self.request.user)

    def form_valid(self, form):
        form.instance.patient = self.request.user.patient_profile
        form.instance.status = 'scheduled'
        return super().form_valid(form)

class AppointmentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointment_form.html'
    success_url = reverse_lazy('appointments')

    def test_func(self):
        appointment = self.get_object()
        return (is_doctor(self.request.user) and appointment.doctor == self.request.user.doctor_profile) or \
               (is_patient(self.request.user) and appointment.patient == self.request.user.patient_profile)

class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy('appointments')

    def test_func(self):
        appointment = self.get_object()
        return (is_doctor(self.request.user) and appointment.doctor == self.request.user.doctor_profile) or \
               (is_patient(self.request.user) and appointment.patient == self.request.user.patient_profile)

class DiagnosisCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'diagnosis_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        return is_doctor(self.request.user)

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor_profile
        return super().form_valid(form)

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        return Review.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем, является ли пользователь пациентом
        try:
            if self.request.user.is_authenticated:
                Patient.objects.get(user=self.request.user)
                context['is_patient'] = True
            else:
                context['is_patient'] = False
        except Patient.DoesNotExist:
            context['is_patient'] = False
        # Добавляем список врачей для формы создания отзыва
        context['doctors'] = Doctor.objects.all()
        return context

class ReviewCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('reviews')

    def test_func(self):
        try:
            Patient.objects.get(user=self.request.user)
            return True
        except Patient.DoesNotExist:
            return False

    def handle_no_permission(self):
        messages.error(self.request, 'Только пациенты могут оставлять отзывы')
        return redirect('reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        try:
            patient = Patient.objects.get(user=self.request.user)
            form.instance.patient = patient
            form.instance.created_at = dj_timezone.now()
            messages.success(self.request, 'Отзыв успешно добавлен')
            return super().form_valid(form)
        except Patient.DoesNotExist:
            messages.error(self.request, 'Профиль пациента не найден')
            return redirect('reviews')

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('reviews')

    def test_func(self):
        review = self.get_object()
        return (self.request.user.is_superuser or 
                (hasattr(self.request.user, 'patient_profile') and 
                 review.patient == self.request.user.patient_profile))

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для редактирования этого отзыва')
        return redirect('reviews')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['doctors'] = Doctor.objects.all()
        return context

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_confirm_delete.html'
    success_url = reverse_lazy('reviews')

    def test_func(self):
        review = self.get_object()
        return (self.request.user.is_superuser or 
                (hasattr(self.request.user, 'patient_profile') and 
                 review.patient == self.request.user.patient_profile))

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого отзыва')
        return redirect('reviews')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Отзыв успешно удален')
        return super().delete(request, *args, **kwargs)

@login_required
def profile(request):
    # Проверяем существование профиля пациента
    try:
        patient_profile = Patient.objects.get(user=request.user)
        appointments = Appointment.objects.filter(patient=patient_profile)
        diagnoses = Diagnosis.objects.filter(patient=patient_profile)
        context = {
            'profile': patient_profile,
            'appointments': appointments,
            'diagnoses': diagnoses,
        }
        return render(request, 'patient_profile.html', context)
    except Patient.DoesNotExist:
        # Если профиля пациента нет, проверяем профиль врача
        try:
            doctor_profile = Doctor.objects.get(user=request.user)
            return redirect('doctor_profile')
        except Doctor.DoesNotExist:
            # Если нет ни одного профиля, создаем новый на основе роли
            if request.user.groups.filter(name='Doctors').exists():
                specialization = Specialization.objects.first()
                if not specialization:
                    messages.error(request, 'Необходимо создать специализации перед созданием профиля врача')
                    return redirect('admin:myapp_specialization_add')
                
                profile = Doctor.objects.create(
                    user=request.user,
                    email=request.user.email,
                    phone='',
                    date_of_birth=dj_timezone.now().date(),
                    education='',
                    experience_years=0
                )
                return redirect('doctor_profile')
            else:
                profile = Patient.objects.create(
                    user=request.user,
                    email=request.user.email,
                    phone='',
                    date_of_birth=dj_timezone.now().date()
                )
                return redirect('profile')

@login_required
def profile_edit(request):
    if hasattr(request.user, 'patient_profile'):
        profile = request.user.patient_profile
        form = PatientProfileForm(instance=profile)
        if request.method == 'POST':
            form = PatientProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен')
                return redirect('profile')
        return render(request, 'profile_edit.html', {'form': form})
    elif hasattr(request.user, 'doctor_profile'):
        profile = request.user.doctor_profile
        form = DoctorProfileForm(instance=profile)
        if request.method == 'POST':
            form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен')
                return redirect('profile')
        return render(request, 'profile_edit.html', {'form': form})
    return HttpResponseForbidden()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['role'] == 'patient':
                try:
                    if not Patient.objects.filter(user=user).exists():
                        Patient.objects.create(
                            user=user,
                            email=user.email,
                            phone=form.cleaned_data['phone'],
                            date_of_birth=form.cleaned_data['date_of_birth']
                        )
                        messages.success(request, 'Регистрация успешна! Теперь вы можете войти в систему.')
                except Exception as e:
                    messages.error(request, 'Произошла ошибка при создании профиля. Пожалуйста, обратитесь к администратору.')
            else:
                try:
                    if not Doctor.objects.filter(user=user).exists():
                        doctor = Doctor.objects.create(
                            user=user,
                            email=user.email,
                            phone=form.cleaned_data['phone'],
                            date_of_birth=form.cleaned_data['date_of_birth'],
                            education=form.cleaned_data['education'],
                            experience_years=form.cleaned_data['experience_years'],
                            photo=form.cleaned_data['photo']
                        )
                        if 'specializations' in form.cleaned_data:
                            doctor.specializations.set(form.cleaned_data['specializations'])
                        messages.success(request, 'Регистрация успешна! Теперь вы можете войти в систему.')
                except Exception as e:
                    messages.error(request, 'Произошла ошибка при создании профиля. Пожалуйста, обратитесь к администратору.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    next_page = 'home'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['password'].widget.attrs.update({'class': 'form-control'})
        return form

    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return super().get_success_url()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

class CustomLogoutView(LogoutView):
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            response = super().dispatch(request, *args, **kwargs)
            messages.success(request, 'Вы успешно вышли из системы')
            return response
        return HttpResponseForbidden()

class DoctorListView(ListView):
    model = Doctor
    template_name = 'doctors.html'
    context_object_name = 'doctors'
    paginate_by = 10

    def get_queryset(self):
        queryset = Doctor.objects.all()
        specialization = self.request.GET.get('specialization')
        if specialization:
            queryset = queryset.filter(specializations=specialization)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['specializations'] = Specialization.objects.all()
        return context

class AboutView(DetailView):
    model = CompanyInfo
    template_name = 'about.html'
    context_object_name = 'company_info'

    def get_object(self):
        return CompanyInfo.objects.first()

class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'doctor_detail.html'
    context_object_name = 'doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        context['appointments'] = Appointment.objects.filter(doctor=doctor)
        context['reviews'] = Review.objects.filter(doctor=doctor)
        return context

class ServiceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        return is_doctor(self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = self.request.user.doctor_profile
        return kwargs

    def form_valid(self, form):
        form.instance.doctor = self.request.user.doctor_profile
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service_form.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        service = self.get_object()
        return is_doctor(self.request.user) and service.doctor == self.request.user.doctor_profile

class ServiceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Service
    success_url = reverse_lazy('profile')
    template_name = 'service_confirm_delete.html'

    def test_func(self):
        service = self.get_object()
        return is_doctor(self.request.user) and service.doctor == self.request.user.doctor_profile

@login_required
def doctor_profile(request):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Эта страница доступна только для врачей')
        return redirect('home')
    
    doctor = request.user.doctor_profile
    services = Service.objects.filter(doctor=doctor)
    
    context = {
        'doctor': doctor,
        'services': services,
    }
    
    return render(request, 'doctor_profile.html', context)

@login_required
def add_service(request):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'У вас нет прав для добавления услуг.')
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes')
        description = request.POST.get('description')
        
        try:
            service = Service.objects.create(
                name=name,
                price=price,
                duration_minutes=duration_minutes,
                description=description,
                doctor=request.user.doctor_profile
            )
            messages.success(request, 'Услуга успешно добавлена.')
            return redirect('doctor_profile')
        except Exception as e:
            messages.error(request, f'Ошибка при добавлении услуги: {str(e)}')
    
    return redirect('doctor_profile')

@login_required
def edit_service(request, service_id):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'У вас нет прав для редактирования услуг.')
        return redirect('home')
    
    service = get_object_or_404(Service, id=service_id, doctor=request.user.doctor_profile)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        duration_minutes = request.POST.get('duration_minutes')
        description = request.POST.get('description')
        
        try:
            service.name = name
            service.price = price
            service.duration_minutes = duration_minutes
            service.description = description
            service.save()
            messages.success(request, 'Услуга успешно обновлена.')
            return redirect('doctor_profile')
        except Exception as e:
            messages.error(request, f'Ошибка при обновлении услуги: {str(e)}')
    
    return redirect('doctor_profile')

@login_required
def delete_service(request, service_id):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Эта страница доступна только для врачей')
        return redirect('home')
    
    service = get_object_or_404(Service, id=service_id, doctor=request.user.doctor_profile)
    
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Услуга успешно удалена')
        return redirect('doctor_profile')
    
    return render(request, 'service_confirm_delete.html', {'service': service})

@login_required
def create_appointment(request):
    # Проверяем, есть ли у пользователя профиль пациента
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.error(request, 'Для записи на прием необходимо создать профиль пациента')
        return redirect('profile_edit')

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        service_id = request.POST.get('service')
        appointment_date = request.POST.get('appointment_date')
        notes = request.POST.get('notes', '')

        try:
            doctor = Doctor.objects.get(id=doctor_id)
            service = Service.objects.get(id=service_id)
            
            # Преобразуем строку даты в datetime с учетом часового пояса
            appointment_datetime = datetime.strptime(appointment_date, '%Y-%m-%dT%H:%M')
            appointment_datetime = dj_timezone.make_aware(appointment_datetime)
            
            # Проверяем, что выбранная дата не в прошлом
            if appointment_datetime < dj_timezone.now():
                messages.error(request, 'Нельзя выбрать дату в прошлом')
                return redirect('create_appointment')

            # Проверяем, что выбранная дата не в выходные
            if appointment_datetime.weekday() >= 5:  # 5 и 6 - суббота и воскресенье
                messages.error(request, 'Запись на выходные дни недоступна')
                return redirect('create_appointment')

            # Проверяем, что выбранное время в рабочее время (9:00 - 18:00)
            if appointment_datetime.hour < 9 or appointment_datetime.hour >= 18:
                messages.error(request, 'Запись доступна только в рабочее время (9:00 - 18:00)')
                return redirect('create_appointment')

            # Проверяем, что нет пересечений с другими записями
            end_time = appointment_datetime + timedelta(minutes=service.duration_minutes)
            overlapping_appointments = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__lt=end_time,
                appointment_date__gt=appointment_datetime - timedelta(minutes=service.duration_minutes)
            )
            if overlapping_appointments.exists():
                messages.error(request, 'Выбранное время уже занято')
                return redirect('create_appointment')

            # Создаем запись
            appointment = Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                service=service,
                appointment_date=appointment_datetime,
                status='scheduled',
                notes=notes
            )

            messages.success(request, 'Запись успешно создана')
            return redirect('appointments')

        except (Doctor.DoesNotExist, Service.DoesNotExist):
            messages.error(request, 'Выбранный врач или услуга не найдены')
            return redirect('create_appointment')
        except Exception as e:
            messages.error(request, f'Произошла ошибка при создании записи: {str(e)}')
            return redirect('create_appointment')

    # GET запрос - показываем форму
    doctors = Doctor.objects.all()
    return render(request, 'appointment_form.html', {
        'doctors': doctors
    })

@login_required
def get_doctor_services(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
        services = Service.objects.filter(doctor=doctor)
        services_data = [{
            'id': service.id,
            'name': service.name,
            'price': float(service.price),
            'duration_minutes': service.duration_minutes
        } for service in services]
        return JsonResponse(services_data, safe=False)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Врач не найден'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def complete_appointment(request, appointment_id):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'У вас нет прав для завершения записи')
        return redirect('appointments')
    
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    
    if request.method == 'POST':
        appointment.status = 'completed'
        appointment.save()
        messages.success(request, 'Запись успешно завершена')
    
    return redirect('appointments')

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Проверяем права доступа
    if not (hasattr(request.user, 'doctor_profile') and appointment.doctor == request.user.doctor_profile) and \
       not (hasattr(request.user, 'patient_profile') and appointment.patient == request.user.patient_profile):
        messages.error(request, 'У вас нет прав для отмены этой записи')
        return redirect('appointments')
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, 'Запись успешно отменена')
    
    return redirect('appointments')

class ArticleListView(ListView):
    model = Article
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 10

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_detail.html'
    context_object_name = 'article'

class CompanyInfoView(DetailView):
    model = CompanyInfo
    template_name = 'company_info.html'
    context_object_name = 'company_info'

    def get_object(self):
        return CompanyInfo.objects.first()

class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news_list'
    paginate_by = 10

class NewsDetailView(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news'

class FAQListView(ListView):
    model = FAQ
    template_name = 'faq.html'
    context_object_name = 'faqs'
    paginate_by = 10

    def get_queryset(self):
        # Сортировка по умолчанию - сначала новые
        return FAQ.objects.all().order_by('-created_at')

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts.html'
    context_object_name = 'contacts'

class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'promocodes.html'
    context_object_name = 'promocodes'
    paginate_by = 10

    def get_queryset(self):
        return PromoCode.objects.filter(
            is_active=True,
            start_date__lte=dj_timezone.now(),
            end_date__gte=dj_timezone.now()
        )

# Статистика
class StatisticsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'statistics.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получаем статистику по услугам
        popular_services = Service.objects.annotate(
            appointment_count=Count('appointments')
        ).order_by('-appointment_count')[:5]
        
        # Получаем статистику по клиентам
        profitable_clients = User.objects.filter(
            patient__appointments__isnull=False
        ).annotate(
            total_spent=Sum('patient__appointments__service__price')
        ).order_by('-total_spent')[:5]
        
        # Получаем статистику по врачам
        profitable_doctors = User.objects.filter(
            doctor_profile__appointments__isnull=False
        ).annotate(
            total_earned=Sum('doctor_profile__appointments__service__price')
        ).order_by('-total_earned')[:5]
        
        # Настройки для всех графиков
        plt.rcParams.update({'font.size': 6})  # Уменьшаем размер шрифта
        
        # График популярных услуг
        plt.figure(figsize=(3, 2))  # Увеличиваем высоту
        services = [service.name for service in popular_services]
        counts = [service.appointment_count for service in popular_services]
        plt.bar(services, counts)
        plt.title('Most Popular Services', fontsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.ylabel('Number of Appointments', fontsize=6)
        
        # Добавляем значения над столбцами
        for i, count in enumerate(counts):
            plt.text(i, count, str(count), ha='center', va='bottom', fontsize=6)
        
        plt.tight_layout()
        
        # Сохраняем первый график
        buffer1 = io.BytesIO()
        plt.savefig(buffer1, format='png', dpi=300, bbox_inches='tight')
        buffer1.seek(0)
        services_graph = base64.b64encode(buffer1.getvalue()).decode('utf-8')
        buffer1.close()
        plt.close()
        
        # График прибыльных клиентов
        plt.figure(figsize=(3, 2))  # Увеличиваем высоту
        clients = [f"{client.first_name} {client.last_name}" for client in profitable_clients]
        spent = [client.total_spent or 0 for client in profitable_clients]
        plt.bar(clients, spent)
        plt.title('Most Profitable Clients', fontsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.ylabel('Total Spent (BYN)', fontsize=6)
        
        # Добавляем значения над столбцами
        for i, amount in enumerate(spent):
            plt.text(i, amount, f"{amount} BYN", ha='center', va='bottom', fontsize=6)
        
        plt.tight_layout()
        
        # Сохраняем второй график
        buffer2 = io.BytesIO()
        plt.savefig(buffer2, format='png', dpi=300, bbox_inches='tight')
        buffer2.seek(0)
        clients_graph = base64.b64encode(buffer2.getvalue()).decode('utf-8')
        buffer2.close()
        plt.close()
        
        # График прибыльных врачей
        plt.figure(figsize=(3, 2))  # Увеличиваем высоту
        doctors = [f"{doctor.first_name} {doctor.last_name}" for doctor in profitable_doctors]
        earned = [doctor.total_earned or 0 for doctor in profitable_doctors]
        plt.bar(doctors, earned)
        plt.title('Most Profitable Doctors', fontsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=6)
        plt.ylabel('Total Earned (BYN)', fontsize=6)
        
        # Добавляем значения над столбцами
        for i, amount in enumerate(earned):
            plt.text(i, amount, f"{amount} BYN", ha='center', va='bottom', fontsize=6)
        
        plt.tight_layout()
        
        # Сохраняем третий график
        buffer3 = io.BytesIO()
        plt.savefig(buffer3, format='png', dpi=300, bbox_inches='tight')
        buffer3.seek(0)
        doctors_graph = base64.b64encode(buffer3.getvalue()).decode('utf-8')
        buffer3.close()
        plt.close()
        
        context.update({
            'services_graph': services_graph,
            'clients_graph': clients_graph,
            'doctors_graph': doctors_graph,
            'popular_services': popular_services,
            'profitable_clients': profitable_clients,
            'profitable_doctors': profitable_doctors,
        })
        
        return context

@login_required
def create_promocode(request):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для создания промокодов')
        return redirect('home')

    if request.method == 'POST':
        form = PromocodeForm(request.POST)
        if form.is_valid():
            promocode = form.save()
            messages.success(request, 'Промокод успешно создан')
            return redirect('promocodes')
    else:
        form = PromocodeForm()
    
    return render(request, 'promocode_form.html', {'form': form, 'action': 'create'})

@login_required
def edit_promocode(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для редактирования промокодов')
        return redirect('home')
    
    promocode = get_object_or_404(PromoCode, pk=pk)
    
    if request.method == 'POST':
        form = PromocodeForm(request.POST, instance=promocode)
        if form.is_valid():
            form.save()
            messages.success(request, 'Промокод успешно обновлен')
            return redirect('promocodes')
    else:
        form = PromocodeForm(instance=promocode)
    
    return render(request, 'promocode_form.html', {'form': form, 'action': 'edit'})

@login_required
def delete_promocode(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'У вас нет прав для удаления промокодов')
        return redirect('home')
    
    promocode = get_object_or_404(PromoCode, pk=pk)
    
    if request.method == 'POST':
        promocode.delete()
        messages.success(request, 'Промокод успешно удален')
        return redirect('promocodes')
    
    return render(request, 'promocode_confirm_delete.html', {'promocode': promocode})

@login_required
def apply_promocode(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            promocode = PromoCode.objects.get(
                code=code,
                is_active=True,
                start_date__lte=dj_timezone.now(),
                end_date__gte=dj_timezone.now()
            )
            # Здесь можно добавить логику применения скидки
            messages.success(request, f'Промокод успешно применен! Скидка: {promocode.discount}%')
        except PromoCode.DoesNotExist:
            messages.error(request, 'Недействительный промокод')
    return redirect('appointments')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 10

    def get_queryset(self):
        queryset = Vacancy.objects.filter(is_active=True)
        q = self.request.GET.get('q')
        sort = self.request.GET.get('sort')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(requirements__icontains=q)
            )
        if sort == 'salary':
            queryset = queryset.order_by('-salary')
        elif sort == 'date':
            queryset = queryset.order_by('-created_at')
        return queryset

class FAQCreateView(CreateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'faq_form.html'
    success_url = reverse_lazy('faq')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            form.fields.pop('category', None)
            form.fields.pop('status', None)
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'pending'
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class FAQUpdateView(LoginRequiredMixin, UpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'faq_form.html'
    success_url = reverse_lazy('faq')

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FAQ.objects.all()
        # Обычные пользователи могут редактировать только свои вопросы
        return FAQ.objects.filter(author=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_superuser:
            # Скрываем поля категории и статуса для обычных пользователей
            form.fields.pop('category', None)
            form.fields.pop('status', None)
        return form

class FAQAnswerView(LoginRequiredMixin, UpdateView):
    model = FAQ
    form_class = FAQForm
    template_name = 'faq_answer_form.html'
    success_url = reverse_lazy('faq')

    def get_queryset(self):
        # Все авторизованные пользователи могут отвечать на любые вопросы
        return FAQ.objects.all()

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Скрываем все поля кроме ответа
        for field in ['question', 'category', 'status']:
            form.fields.pop(field, None)
        return form

    def form_valid(self, form):
        # Устанавливаем автора ответа
        form.instance.answer_author = self.request.user
        return super().form_valid(form)

class FAQDeleteAnswerView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_superuser:
            return HttpResponseForbidden()
        
        faq = get_object_or_404(FAQ, pk=pk)
        faq.answer = None
        faq.answer_author = None
        faq.save()
        
        messages.success(request, 'Ответ успешно удален')
        return redirect('faq')

class FAQDeleteView(LoginRequiredMixin, DeleteView):
    model = FAQ
    success_url = reverse_lazy('faq')
    template_name = 'faq_confirm_delete.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return FAQ.objects.all()
        return FAQ.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        faq = self.get_object()
        if request.user.is_superuser and 'delete_answer' in request.POST:
            # Если суперпользователь удаляет только ответ
            faq.answer = None
            faq.answer_author = None
            faq.save()
            return HttpResponseRedirect(self.success_url)
        return super().delete(request, *args, **kwargs)

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsCreateView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'news_form.html'
    fields = ['title', 'short_content', 'content', 'image']
    success_url = reverse_lazy('news')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsUpdateView(LoginRequiredMixin, UpdateView):
    model = News
    template_name = 'news_form.html'
    fields = ['title', 'short_content', 'content', 'image']
    success_url = reverse_lazy('news')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class NewsDeleteView(LoginRequiredMixin, DeleteView):
    model = News
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class VacancyCreateView(LoginRequiredMixin, CreateView):
    model = Vacancy
    fields = ['title', 'description', 'requirements', 'salary', 'is_active']
    template_name = 'vacancy_form.html'
    success_url = reverse_lazy('vacancies')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class VacancyUpdateView(LoginRequiredMixin, UpdateView):
    model = Vacancy
    fields = ['title', 'description', 'requirements', 'salary', 'is_active']
    template_name = 'vacancy_form.html'
    success_url = reverse_lazy('vacancies')

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class VacancyDeleteView(LoginRequiredMixin, DeleteView):
    model = Vacancy
    template_name = 'vacancy_confirm_delete.html'
    success_url = reverse_lazy('vacancies')

class CompanyInfoUpdateView(UserPassesTestMixin, UpdateView):
    model = CompanyInfo
    fields = ['title', 'content', 'logo']
    template_name = 'company_info_form.html'
    success_url = reverse_lazy('about')

    def test_func(self):
        return self.request.user.is_superuser

    def get_object(self, queryset=None):
        return CompanyInfo.objects.first()

class PromoCodeCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = PromoCode
    template_name = 'promocode_form.html'
    fields = ['code', 'discount', 'end_date', 'is_active']
    success_url = reverse_lazy('promocodes')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Промокод успешно создан')
        return super().form_valid(form)

class PromoCodeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = PromoCode
    template_name = 'promocode_form.html'
    fields = ['code', 'discount', 'end_date', 'is_active']
    success_url = reverse_lazy('promocodes')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        messages.success(self.request, 'Промокод успешно обновлен')
        return super().form_valid(form)

class PromoCodeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PromoCode
    template_name = 'promocode_confirm_delete.html'
    success_url = reverse_lazy('promocodes')

    def test_func(self):
        return self.request.user.is_superuser

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Промокод успешно удален')
        return super().delete(request, *args, **kwargs)
