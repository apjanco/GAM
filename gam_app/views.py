from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from gam_app import advanced_search


# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
	return render(request, 'index.html')

def document(request, filename):
	state = get_object_or_404(Imagen, nombre_del_archivo=filename)
	context  = {'state':state}
	return render(request, 'document_page.html', context)

def document_edit(request, filename):
	state = get_object_or_404(Imagen, nombre_del_archivo=filename)
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

#TODO: this section works, but should be revised by someone with a more-than-basic understanding of Django
#documento5 is a hack that only works with the desapareccidos collection and GAM archive
#using a simple get() raises: 'The QuerySet value for an exact lookup must be limited to one result using slicing.'
#No help on SO or elsewhere (APJ 1/10/18)
def documento5(request, archivo, colección, caja, legajo, carpeta, número_de_imagen):
	id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for a in id:
		archivo5_id = id

	id = Colección.objects.filter(nombre_de_la_colección=colección)
	for b in id:
		colección5_id = id
	localizacion_fisica = caja +'_'+ legajo +'_'+ carpeta +'_'+ número_de_imagen
	state = get_object_or_404(Imagen, localizacion_fisica=localizacion_fisica)
	context = {'state':state}
	return render(request, 'document_page.html', context)

def documento4(request, archivo, colección, caja, legajo, carpeta):

	a_id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for a in a_id:
		archivo4_id = a.id

	c_id = Colección.objects.filter(nombre_de_la_colección=colección)
	for b in c_id:
		colección4_id = b.id

	state = Imagen.objects.filter(archivo=archivo4_id, colección=colección4_id, caja=caja, legajo=legajo, carpeta=carpeta)	
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)

def documento3(request, archivo, colección, caja, legajo):
	
	a_id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for a in a_id:
		archivo3_id = a.id

	c_id = Colección.objects.filter(nombre_de_la_colección=colección)
	for b in c_id:
		colección3_id = b.id

	state = Imagen.objects.filter(archivo=archivo3_id, colección=colección3_id, caja=caja, legajo=legajo)	
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)

def documento2(request, archivo, colección, caja):
	a_id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for a in a_id:
		archivo2_id = a.id

	c_id = Colección.objects.filter(nombre_de_la_colección=colección)
	for b in c_id:
		colección2_id = b.id

	state = Imagen.objects.filter(archivo=archivo2_id, colección=colección2_id, caja=caja)	
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)

def documento1(request, archivo, colección):
	
	a_id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for a in a_id:
		archivo1_id = a.id

	c_id = Colección.objects.filter(nombre_de_la_colección=colección)
	for b in c_id:
		colección1_id = b.id

	state = Imagen.objects.filter(archivo=archivo1_id, colección=colección1_id)	
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)

def documento0(request, archivo):
	id = Archivo.objects.filter(nombre_del_archivo=archivo)
	for i in id:
		archivo0_id = i.id
	state = Imagen.objects.filter(archivo=archivo0_id)	
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)


	

		
