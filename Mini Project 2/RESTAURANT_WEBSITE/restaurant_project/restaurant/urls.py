from django.urls import path
from . import views
from .views import user_login, user_register, user_logout

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('reservation/', views.reservation, name='reservation'),
    path('feedback/', views.feedback, name='feedback'),
    path('login/',user_login, name='login'),
    path('register/',user_register, name='register'),
    path('logout/', user_logout, name='logout'),
]
