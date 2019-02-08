from django.urls import path

from . import views

from django.urls import include

app_name = "acceso"

urlpatterns = [path('investigación/', views.main, name='main')]
