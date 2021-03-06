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
from django.urls import path
from gam_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('search_results/', views.search, name='search'),
    path('file/<filename>', views.document, name='document'),
    path('edit/<filename>', views.document_edit, name='document_edit'),
    path('dzi/<file>', views.dzi, name='dzi'),
    path('caso/', views.caso, name='caso'),
    path('advanced_search_submit/', views.advanced_search_submit, name='advanced-search-submit'),
    path('sobre/', views.sobre, name='sobre'),
    path('documentos/', views.all_documents, name='all_documents'),
    path('multi/', views.multi_image, name='multi_image'),
    path('texto/', views.todo_texto, name='all_texto'),
    path('caso/<caso>', views.single_caso, name='single_caso'),

    



]
