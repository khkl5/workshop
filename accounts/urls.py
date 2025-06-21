from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),
]
