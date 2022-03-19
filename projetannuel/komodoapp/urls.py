from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vm_deploy', views.vm_deploy, name='vm_deploy'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout')
]