"""archivo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include, url
from gam_app import views
from django.contrib.flatpages import views as flat_views
from dal import autocomplete
from django.contrib.auth.decorators import login_required

#from gam_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.hmac.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    path('acceso/', include('acceso.urls')),
    path('buscar/', views.search, name='search'),
    path('cuentas/', include('django.contrib.auth.urls')),
    path('control-de-misión/', views.mission_control, name='mission_control'),
    path('item/<nombre_del_item>/', views.item, name='item'),
    path('track-bags/', views.track_bags, name='track_bags'),
    path('datatable/imagen', login_required(views.ImagenListJson.as_view()), name='imagen_list_json'),
    path('datatable/imagen_desc', login_required(views.ImagenListDescJson.as_view()), name='imagen_desc_list_json'),
    path('datatable/carpeta', login_required(views.CarpetaListJson.as_view()), name='carpeta_list_json'),
    path('datatable/carpeta_buscar', login_required(views.CarpetaListJson_Buscar.as_view()), name='carpeta_list_json_buscar'),
    path('autocompletar_imagen/', views.ImageFieldAutocomplete.as_view(), name='autocompletar_imagen'),
    path('persona/create/', views.PersonaCreate.as_view(), name='persona_create'),
    path('persona/<int:pk>/update/', views.PersonaUpdate.as_view(), name='persona_update'),
    path('persona/<int:pk>', views.PersonaDetailView.as_view(), name='persona_detail'),
    path('personalookup/', views.PersonaNameLookup.as_view(), name='persona_name_lookup'),
    path('lugar/create/', views.LugarCreate.as_view(), name='lugar_create'),
    path('lugar/<int:pk>/update/', views.LugarUpdate.as_view(), name='lugar_update'),
    path('lugarlookup/', views.LugarNameLookup.as_view(), name='lugar_name_lookup'),
    path('organizacion/create/', views.OrganizacionCreate.as_view(), name='organizacion_create'),
    path('organizacion/<int:pk>/update/', views.OrganizacionUpdate.as_view(), name='organizacion_update'),
    path('organizacionlookup/', views.OrganizacionNameLookup.as_view(), name='organizacion_name_lookup'),
    path('autocompletar_manuscrito/', views.autocompletar_manuscrito.as_view(), name='autocompletar_manuscrito'),
    path('crear_usuario/', include('registration.backends.simple.urls')),
    path('advanced_search_submit/', views.advanced_search_submit, name='advanced-search-submit'),
    path('sobre/', flat_views.flatpage, {'url': '/es/sobre/'}, name='sobre'),
    path('about/', flat_views.flatpage, {'url': '/en/about/'}, name='about'),
    path('über/', flat_views.flatpage, {'url': '/de/über/'}, name='über'),
    path('explorar/', views.explorar, name='explorar'),
    path('lugar/<lugar>', views.lugar, name='lugar'),
    path('procesamiento/<archivo>/<colección>/<caja>/<legajo>/<carpeta>/', views.procesamiento, name='procesamiento'),
    #paths for working with images (personal is 'staff')
    path('imagen/<archivo>/<colección>/<caja>/<legajo>/<carpeta>/<número_de_imagen>/', views.documento5, name='documento5'),
    path('imagen/<archivo>/<colección>/<caja>/<legajo>/<carpeta>/', views.documento4, name='documento4'),
    path('imagen/<archivo>/<colección>/<caja>/<legajo>/', views.documento3, name='documento3'),
    path('imagen/<archivo>/<colección>/<caja>/', views.documento2, name='documento2'),
    path('imagen/<archivo>/<colección>/', views.documento1, name='documento1'),
    path('imagen/<archivo>/', views.documento0, name='documento0'),
)
