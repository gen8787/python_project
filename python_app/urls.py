from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('go_login', views.go_login),
    path('register', views.register),
    path('go_register', views.go_register),

    path('dashboard', views.dashboard),

    path('add_route', views.add_route),

    path('logout', views.logout)
]