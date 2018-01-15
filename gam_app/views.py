from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from gam_app import advanced_search
from django.template import RequestContext
from gam_app.forms import EditForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
	return render(request, 'index.html')

def document(request, filename):
	if request.method == 'POST':
		form = EditForm(request.POST)
		if form.is_valid():
			print(request.POST)
			texto_de_OCR = request.POST['texto_de_OCR']
			file = request.POST.get('nombre_del_archivo', None)

			#form.archivo = 4
			#form.save(commit=True)
			Imagen.objects.update_or_create(
                            nombre_del_archivo = file,
                            texto_de_OCR = texto_de_OCR,
                            )

			state = get_object_or_404(Imagen, nombre_del_archivo=filename)
			context  = {'state':state, 'form':form}
			return render(request, 'document_page.html', context)
		else:
			print(form.errors)
	else:
		state = get_object_or_404(Imagen, nombre_del_archivo=filename)
		id = state.id
		form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})
		context  = {'state':state, 'form':form,'id':id}		
		return render(request, 'document_page.html', context)

def document_edit(request, filename):
	state = get_object_or_404(Imagen, nombre_del_archivo=filename)
	return render(request, 'document_edit_page.html',{'state':state})

def lugar(request, lugar):
	l_id = Lugar.objects.filter(nombre_del_lugar=lugar)
	for a in l_id:
                lugar_id = a.id
	lugar_id = lugar_id
	state = Imagen.objects.filter(ubicación_geográfica=lugar_id)
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)

def persona(request, nombre):
	p_id = Persona.objects.filter(nombre_de_la_persona=nombre)
	for p in p_id:
		persona_id = p.id
	persona_id = persona_id
	state = Imagen.objects.filter(persona=persona_id)
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)
 

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

@login_required
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


def documento5(request, archivo, colección, caja, legajo, carpeta, número_de_imagen):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta, número_de_imagen=número_de_imagen)	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja, 'legajo':legajo, 'carpeta':carpeta, 'número_de_imagen':número_de_imagen}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

def documento4(request, archivo, colección, caja, legajo, carpeta):

	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta)	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja, 'legajo':legajo, 'carpeta':carpeta}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

def documento3(request, archivo, colección, caja, legajo):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo)	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja, 'legajo':legajo}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

def documento2(request, archivo, colección, caja):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja)	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

def documento1(request, archivo, colección):
	

	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección)	
	location = {'archivo':archivo, 'colección':colección}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

def documento0(request, archivo):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo)
	location = {'archivo':archivo}
	context = {'state':state,'location':location}
	return render(request, 'all_documents_page.html', context)



		
