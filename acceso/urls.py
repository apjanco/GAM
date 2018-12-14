from django.urls import path, re_path

from . import views
from .views import casoTable

from django.urls import include

app_name = "acceso"

urlpatterns = [
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('map/', views.map, name='map'),
    path('caso/<caso>', views.caso, name='caso'),
    path('simple/', views.simple, name='simple'),

    # jsGrid
    path('caso-index/', views.caso_index, name='caso_index'),
    path('api/', casoTable.as_view()),
    re_path(r'api/(?P<caso_id>[0-9])/$', casoTable.as_view()),
]
