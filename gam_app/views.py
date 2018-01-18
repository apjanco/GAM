from django.shortcuts import render
from .models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from gam_app import advanced_search
from django.template import RequestContext
from gam_app.forms import EditForm, SearchForm, PortapapelesForm
from django.contrib.auth.decorators import login_required
import datetime
from django.contrib.auth.models import User

#search engine dependencies 
from elasticsearch_django.settings import get_client
from elasticsearch_django.models import SearchQuery
#from elasticsearch_dsl import Search

# Create your views here.

def index(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		query = request.POST.get('search', None)
		if form.is_valid():
			state = Imagen.objects.filter(texto_de_OCR__icontains=query)
			context  = {'state':state, 'form':form}
			return render(request, 'all_documents_page.html', context)
		else:
			print(form.errors)
	else:
		search = ""
		form = SearchForm(initial={'search': search })
	return render(request, 'index.html', {'form':form})

def search(request, query):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			state = Imagen.objects.filter(texto_de_OCR__icontains=query)
			context  = {'state':state, 'form':form}
			return render(request, 'all_documents_page.html', context)
		else:
			print(form.errors)
	else:
		search = "Buscar..."
		form = SearchForm(initial={'search': search })
	return render(request, 'index.html', {'form':form})

def elasticsearch(request, query):
	search = Search(using=get_client(), index='gam')
	state = SearchQuery.execute(search)
	for obj in Imagen.objects.from_search_query(sq):
		print(obj.search_score, obj.search_rank)
		context  = {'state':state}
	return render(request, 'all_documents_page.html', context)

@login_required
def document(request, filename):
	
	if request.method == 'POST':
		if request.POST['input'] == 'text_edit':
			edit_form = EditForm(request.POST)
			if edit_form.is_valid():
				texto_de_OCR = request.POST['texto_de_OCR']
				file = request.POST.get('nombre_del_archivo', None)
				archivo = get_object_or_404(Archivo, nombre_del_archivo=request.POST.get('archivo', None))	
				archivo_id = archivo.id
				collection = get_object_or_404(Colección, nombre_de_la_colección=request.POST.get('colección', None))
				box = request.POST.get('caja', None)
				bundle = request.POST.get('legajo', None)
				folder = request.POST.get('carpeta', None)
				old_text = request.POST.get('old_text', None)
				time = datetime.datetime.now()
				usuario_id = User.objects.get(username=request.user).pk
				#save previous text 
				transcription = Transcrito(usuario_id=usuario_id, nombre_del_archivo=file, tiempo_modificado=time, texto_transcrito=old_text) 
				transcription.save()

				#save with the new data
				image = Imagen.objects.get(nombre_del_archivo = file)
				image.texto_de_OCR = texto_de_OCR
				image.save() 
				
				state = get_object_or_404(Imagen, nombre_del_archivo=filename)
				context  = {'state':state, 'form':edit_form}
				return render(request, 'document_page.html', context)
			
			else:
				print(form.errors)

		if request.POST['input'] == 'clipboard':
			clip_form = PortapapelesForm(request.POST)
			if clip_form.is_valid():
				print ('Clipboard!')
				state = get_object_or_404(Imagen, nombre_del_archivo=filename)
				id = state.id
				context  = {'state':state, 'clipboard':clip_form,'id':id}		
				return render(request, 'document_page.html', context)

	else:
		state = get_object_or_404(Imagen, nombre_del_archivo=filename)
		id = state.id
		form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})
		clip_form = PortapapelesForm(request.POST)
		context  = {'state':state, 'form':form, 'clipboard':clip_form, 'id':id}		
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

def persona(request, persona):
	state = Imagen.objects.filter(persona__nombre_de_la_persona=persona)
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)
 

def all_documents(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		query = request.POST.get('search', None)
		if form.is_valid():
			state = Imagen.objects.filter(texto_de_OCR__icontains=query)
			context  = {'state':state, 'form':form}
			return render(request, 'all_documents_page.html', context)
		else:
			print(form.errors)
	else:
		state = Imagen.objects.all()
		search = ""
		form = SearchForm(initial={'search': search })
		context = {'state':state,'form':form }
	return render(request, 'all_documents_page.html', context)

def todo_texto(request):
	state = Imagen.objects.all()
	context  = {'state':state}
	return render(request, 'todo_texto.html', context)

@login_required
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

@login_required
def documento0(request, archivo):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		query = request.POST.get('search', None)
		if form.is_valid():
			state = Imagen.objects.filter(texto_de_OCR__icontains=query)
			context  = {'state':state, 'form':form}
			return render(request, 'all_documents_page.html', context)
		else:
			print(form.errors)
	else:
		search = ""
		form = SearchForm(initial={'search': search })
		state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo)
		location = {'archivo':archivo}
		context = {'state':state,'form':form, 'location':location }
		
		return render(request, 'all_documents_page.html', context)



		
