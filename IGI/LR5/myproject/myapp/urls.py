from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('services/', views.ServiceListView.as_view(), name='services'),
    path('services/create/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/update/', views.ServiceUpdateView.as_view(), name='service_update'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),
    path('doctors/', views.DoctorListView.as_view(), name='doctors'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('reviews/', views.ReviewListView.as_view(), name='reviews'),
    path('reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('about/', views.CompanyInfoView.as_view(), name='about'),
    path('about/edit/', views.CompanyInfoUpdateView.as_view(), name='company_info_update'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointments'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment_update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointments/<int:appointment_id>/complete/', views.complete_appointment, name='appointment_complete'),
    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='appointment_cancel'),
    path('diagnoses/create/', views.DiagnosisCreateView.as_view(), name='diagnosis_create'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/doctor/', views.doctor_profile, name='doctor_profile'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('services/add/', views.add_service, name='add_service'),
    path('services/<int:service_id>/edit/', views.edit_service, name='edit_service'),
    path('services/<int:service_id>/delete/', views.delete_service, name='delete_service'),
    path('api/doctor-services/<int:doctor_id>/', views.get_doctor_services, name='get_doctor_services'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('company/', views.CompanyInfoView.as_view(), name='company_info'),
    path('news/', views.NewsListView.as_view(), name='news'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),
    path('faq/', views.FAQListView.as_view(), name='faq'),
    path('faq/create/', views.FAQCreateView.as_view(), name='faq_create'),
    path('faq/<int:pk>/update/', views.FAQUpdateView.as_view(), name='faq_update'),
    path('faq/<int:pk>/answer/', views.FAQAnswerView.as_view(), name='faq_answer'),
    path('faq/<int:pk>/delete/', views.FAQDeleteView.as_view(), name='faq_delete'),
    path('faq/<int:pk>/delete-answer/', views.FAQDeleteAnswerView.as_view(), name='faq_delete_answer'),
    path('contacts/', views.ContactListView.as_view(), name='contacts'),
    path('vacancies/', views.VacancyListView.as_view(), name='vacancies'),
    path('promocodes/', views.PromoCodeListView.as_view(), name='promocodes'),
    path('promocodes/create/', views.PromoCodeCreateView.as_view(), name='promocode_create'),
    path('promocodes/<int:pk>/update/', views.PromoCodeUpdateView.as_view(), name='promocode_update'),
    path('promocodes/<int:pk>/delete/', views.PromoCodeDeleteView.as_view(), name='promocode_delete'),
    path('promocodes/apply/', views.apply_promocode, name='apply_promocode'),
    path('statistics/', views.StatisticsView.as_view(), name='statistics'),
    path('privacy/', views.privacy_policy, name='privacy_policy'),
    path('vacancies/create/', views.VacancyCreateView.as_view(), name='vacancy_create'),
    path('vacancies/<int:pk>/edit/', views.VacancyUpdateView.as_view(), name='vacancy_edit'),
    path('vacancies/<int:pk>/delete/', views.VacancyDeleteView.as_view(), name='vacancy_delete'),
]