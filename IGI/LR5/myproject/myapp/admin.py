from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Patient,
    Doctor,
    Specialization,
    ServiceCategory,
    Service,
    Appointment,
    Diagnosis,
    Review,
    Article,
    CompanyInfo,
    CompanyHistory,
    News,
    FAQ,
    Contact,
    Vacancy,
    PromoCode
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль пользователя'

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_middle_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'userprofile__middle_name')

    def get_middle_name(self, obj):
        return obj.profile.middle_name
    get_middle_name.short_description = 'Отчество'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__userprofile__middle_name')
    list_filter = ('date_of_birth',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_specializations', 'experience_years', 'phone')
    list_filter = ('specializations', 'experience_years')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone')
    filter_horizontal = ('specializations',)
    fieldsets = (
        ('Личная информация', {
            'fields': ('user', 'phone', 'date_of_birth', 'photo')
        }),
        ('Профессиональная информация', {
            'fields': ('specializations', 'experience_years', 'education')
        }),
    )

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'ФИО'

    def get_specializations(self, obj):
        return ", ".join([spec.name for spec in obj.specializations.all()])
    get_specializations.short_description = 'Специализации'

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes')
    list_filter = ('duration_minutes',)
    search_fields = ('name', 'description')
    list_editable = ('price',)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'service', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date', 'doctor')
    search_fields = ('patient__user__username', 'doctor__user__username', 'service__name')

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'name', 'date')
    list_filter = ('date', 'doctor')
    search_fields = ('patient__user__username', 'doctor__user__username', 'name', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'doctor')
    search_fields = ('patient__user__username', 'doctor__user__username', 'text')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_content', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    search_fields = ('title', 'content')

@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('year', 'description', 'company_info')
    list_filter = ('year', 'company_info')
    search_fields = ('description',)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'answer')
    date_hierarchy = 'created_at'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'phone', 'email')
    search_fields = ('name', 'position', 'email')
    list_filter = ('position',)

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'end_date')
    search_fields = ('code',)
    date_hierarchy = 'end_date'