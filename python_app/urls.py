from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('go_login', views.go_login),
    path('register', views.register),
    path('go_register', views.go_register),
    path('dashboard', views.dashboard),
    path('validate_trail',views.validate_trail),
    path('create_trail', views.create_trail),
    path('logout', views.logout)
]