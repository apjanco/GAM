from django.urls import path

from . import views

from django.urls import include

app_name = "acceso"

urlpatterns = [
    path('', views.main,{'options': True},name='index'),
    path('table/', views.main,{'options': False},name='table'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('map/', views.map, name='map'),
    path('caso/<caso>', views.caso, name='caso'),
    path('simple/', views.simple, name='simple'),
]
