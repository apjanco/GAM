from django.urls import path, re_path

from . import views

from django.urls import include

app_name = "acceso"

urlpatterns = [
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('map/', views.map, name='map'),
    path('caso/<caso>', views.caso, name='caso'),
    path('simple/', views.simple, name='simple'),
    path('network_json/', views.network_json, name='network_json'),
    path('network', views.network, name='network'),
    # jsGrid
    path('caso-index/', views.caso_index, name='caso_index'),
    path('api/<int:caso_id>/', views.caso_table),
]
