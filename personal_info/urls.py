
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.LoginView, name="login_view"),
    path('apply/', views.ApplyView, name="apply"),
]