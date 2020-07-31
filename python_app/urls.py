from django.urls import path
from . import views

urlpatterns = [
    path('',views.login),
    path('go_login', views.go_login),
    path('register', views.register),
    path('go_register', views.go_register),

    path('dashboard', views.dashboard),

    path('view_climbs', views.view_climbs),
    path('remove_climb/<int:trail_id>', views.remove_climb),

    path('add_route/<int:route_id>', views.add_route),

    path('validate_trail',views.validate_trail),
    path('create_trail', views.create_trail),

    path('logout', views.logout)
]