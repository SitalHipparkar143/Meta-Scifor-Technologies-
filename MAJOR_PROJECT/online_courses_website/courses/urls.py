from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # 👈 Default page is login
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('enroll/<int:course_id>/', views.enroll_in_course, name='enroll_in_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
] + static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
