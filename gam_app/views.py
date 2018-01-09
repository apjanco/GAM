# -*- coding: utf-8 -*-
from django.shortcuts import render
from .models import Imagen, Caso
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from gam_app import advanced_search


# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
	return render(request, 'index.html')

def document(request, filename):
	state = get_object_or_404(Imagen, filename=nombre_del_archivo)
	context  = {'state':state}
	return render(request, 'document_page.html', context)

def document_edit(request, filename):
	state = get_object_or_404(Imagen, filename=nombre_del_archivo)
	return render(request, 'document_edit_page.html',{'state':state})

def all_documents(request):
	state = Imagen.objects.all()
	context  = {'state':state}
	return render(request, 'all_documents_page.html', context)

def todo_texto(request):
	state = Imagen.objects.all()
	context  = {'state':state}
	return render(request, 'todo_texto.html', context)

def multi_image(request):
        state = Imagen.objects.all()
        context  = {'state':state}
        return render(request, 'document_multi_image.html', context)

def dzi(request, file):
	file = open('/srv/GAM/gam_app/dzis/%s.dzi' % file)
	response = HttpResponse(content=file)
	return response 

def caso(request):
	state = Caso.objects.all()
	context  = {'state':state}
	return render(request, 'caso_page.html', context)

def single_caso(request, caso):
	state = get_object_or_404(Caso, caso=caso)
	context  = {'state':state}
	return render(request, 'single_caso_page.html', context)

def sobre(request):
	return render(request, 'about.html')

def advanced_search_submit(request):
    context = advanced_search.advanced_search(request)
    if context:
        return render(request, 'search.html', context)
    else:
        context = {"failed" : True}
        return render(request, 'index.html', context)
