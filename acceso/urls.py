from django.urls import path, re_path
from django.contrib.auth.decorators import login_required


from . import views

from django.urls import include

app_name = "acceso"

urlpatterns = [
    path('', views.main, name='index'),
    path('about/', views.about, name='about'),
    path('history/', views.history, name='history'),
    path('colección/', views.collection, name='collection'),
    path('caso/<caso>', views.caso, name='caso'),
    path('simple/', views.simple, name='simple'),
    path('skynet/', views.skynet, name='skynet'),

    # jsGrid
    path('caso-index/', views.caso_index, name='caso_index'),
    path('buscador-de-casos/', views.datatable, name='buscador-de-casos'),
    path('api/<int:caso_id>/', views.caso_table),
    path(
        'datatable_caso/',
        views.DbListJson.as_view(),
        name='db_list_json',
    ),
    path('documentos/', views.documentos, name='documentos'),
]
