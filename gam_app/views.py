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
from dal import autocomplete

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
				#print('this is the request',request)
				texto_de_OCR = request.POST['texto_de_OCR']
				file = request.POST.get('nombre_del_archivo', None)
				archivo = get_object_or_404(Archivo, nombre_del_archivo=request.POST.get('archivo', None))	
				archivo_id = archivo.id
				collection = get_object_or_404(Colección, nombre_de_la_colección=request.POST.get('colección', None))
				box = request.POST.get('caja', None)
				bundle = request.POST.get('legajo', None)
				folder = request.POST.get('carpeta', None)
				old_text = request.POST.get('old_text', None)
				notas = request.POST.get('notas', None)
				persona = request.POST.get('persona', None)
				print('here is the person')
				print(persona)

				lugar = request.POST.get('ubicación_geográfica', None)
				actividades_políticas = request.POST.get('actividades_políticas', None)
				fecha_desaparicion = request.POST.get('fecha_desaparicion', None)
				genero = request.POST.get('genero', None)
				manuscritos = request.POST.get('manuscripts', None)
				
				time = datetime.datetime.now()
				usuario_id = User.objects.get(username=request.user).pk
				#save previous text 
				transcription = Transcrito(usuario_id=usuario_id, nombre_del_archivo=file, tiempo_modificado=time, texto_transcrito=old_text) 
				transcription.save()

				#save with the new data
				image = Imagen.objects.get(nombre_del_archivo = file)
				image.texto_de_OCR = texto_de_OCR
				image.notas = notas
				image.persona = persona
				image.ubicación_geográfica.add(lugar)
				image.actividades_políticas.add(actividades_políticas)
				image.género.add(genero)
				image.manuscritos.add(manuscritos)
				image.save() 


				clipboard = PortapapelesForm(request.POST)
				 
				
				state = get_object_or_404(Imagen, nombre_del_archivo=filename)
				context  = {'state':state, 'form':edit_form, 'clipboard':clipboard}
				return render(request, 'document_page.html', context)
			
			else:
				print(form.errors)

		if request.POST['input'] == 'clipboard':
			clipboard = PortapapelesForm(request.POST)
			if clipboard.is_valid():
				response = dict(clipboard.data)
				choice = response.get('list_name', None)
				print('choice',choice)
				clipboards = Portapapeles.objects.all()
				print('clipboards',clipboards)
				chosen = clipboards[int(choice[0])-1]
				#print(chosen)
				user = response.get('user', None)
				file = response.get('filename', None)
				print ('Clipboard!', dict(clipboard.data))
				user_id = User.objects.get(username=user[0]).pk
				clip = Portapapeles.objects.get(nombre_del_portapapeles=chosen, usuario=user_id)
				clip.imágenes.add(Imagen.objects.get(nombre_del_archivo=file[0]).pk) 
				clip.save()

				state = get_object_or_404(Imagen, nombre_del_archivo=filename)
				id = state.id
				form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})

				context  = {'state':state,'form':form,'clipboard':clipboard,'id':id}		
				return render(request, 'document_page.html', context)

	else:
		state = get_object_or_404(Imagen, nombre_del_archivo=filename)
		#TODO add forward + backward buttons
		possible_pages = Imagen.objects.filter(archivo__nombre_del_archivo=state.archivo, colección__nombre_de_la_colección=state.colección, caja=state.caja, legajo=state.legajo, carpeta=state.carpeta).order_by('número_de_imagen')	
		pages_list = []
		for index, page in enumerate(possible_pages):
			pages_list.append(page)

			#print(index, page)
			if page == state:
				print('current= ', page.número_de_imagen, index)
				current = int(index)
		previous = pages_list[current-1].número_de_imagen
		try:
			next_one = pages_list[current+1].número_de_imagen
		except:
			next_one = pages_list[current].número_de_imagen

		print('previous= ', previous)
		print('next= ', next_one)
		#next_one = pages_list[int(current)+1]
		#print(current, next_one, previous)
			#print(index, page)
			#if page == state:
			#	print('this is it', page.número_de_imagen, index)
		#		current = index
		#	next_one = current + 1, page
		#	print(next_one) 
			#print (possible_pages)

		id = state.id
		form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})
		clipboard = PortapapelesForm(request.POST)
		context  = {'state':state, 'form':form, 'clipboard':clipboard, 'id':id, 'previous':previous, 'next_one':next_one}		
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

#These are the views for the autocomplete fields in document_page.html 
class autocompletar(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#TODO Get working with user authentication
		#if not self.request.user.is_authenticated():
	#		return Imagen.objects.none()
		
		qs = Persona.objects.all()

		if self.q:
			qs = qs.filter(nombre_de_la_persona__icontains=self.q)
		
		return qs

class autocompletar_lugar(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#TODO Get working with user authentication
		#if not self.request.user.is_authenticated():
	#		return Imagen.objects.none()
		
		qs = Lugar.objects.all()

		if self.q:
			qs = qs.filter(nombre_del_lugar__icontains=self.q)
		
		return qs

class autocompletar_organización(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		#TODO Get working with user authentication
		#if not self.request.user.is_authenticated():
	#		return Imagen.objects.none()
		
		qs = Organización.objects.all()#.values_list('nombre_de_la_organización', flat=True)
		
		if self.q:
			qs = qs.filter(nombre_de_la_organización__icontains=self.q)
		
		return qs

class autocompletar_manuscrito(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Manuscrito.objects.all()
        if self.q:
            qs = qs.filter(nombre_del_manuscrito__icontains=self.q)
        return qs

def persona(request, persona):
	state = Imagen.objects.filter(persona__nombre_de_la_persona=persona)
	context = {'state':state}
	return render(request, 'all_documents_page.html', context)
 
@login_required
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

@login_required
def todo_texto(request):
	state = Imagen.objects.all()
	context  = {'state':state}
	return render(request, 'todo_texto.html', context)

#These two views work with the clipboard.  The first takes a url with portapaeles and an
#the name of a clipboard.  It then returns the name of the clipboard and all images in it.
def espacio_de_trabajo(request, portapapeles):
	clipboard = Portapapeles.objects.filter(nombre_del_portapapeles=portapapeles)
	state = Imagen.objects.filter(portapapeles__nombre_del_portapapeles=portapapeles)
	context  = {'state':state, 'clipboards':clipboard }
	return render(request, 'document_multi_image.html', context)

#This one renders a list of all clipboards.  Note that both views share the same template. 
@login_required
def portapapeles(request):
	clipboards = Portapapeles.objects.all()
	state = Imagen.objects.all()
	context  = {'state':state, 'clipboards':clipboards}
	return render(request, 'document_multi_image.html', context)

def dzi(request, file):
	file = open('/srv/GAM/gam_app/dzis/%s.dzi' % file)
	response = HttpResponse(content=file)
	return response 

@login_required
def explorar(request):
	state = Imagen.objects.all()
	archives = Archivo.objects.all()
	collections = Imagen.objects.values('archivo__nombre_del_archivo','colección__nombre_de_la_colección').distinct()
	for collection in collections:
		collection['descripción'] = get_object_or_404(Colección, nombre_de_la_colección= collection['colección__nombre_de_la_colección']).descripción
	
	carpetas = Imagen.objects.values('archivo__nombre_del_archivo','colección__nombre_de_la_colección', 'caja', 'legajo', 'carpeta').distinct()
	#for carpeta in carpetas:
	#	print(carpeta)
#		carpeta['descripción'] = get_object_or_404(Carpeta, archivo=carpeta['archivo__nombre_del_archivo'], carpeta_no= carpeta['carpeta']).descripcion_caso

	context  = {'state':state, 'archives':archives, 'collections':collections, 'carpetas':carpetas}
	return render(request, 'explorar.html', context)


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
        context['state'] = context['results']
        return render(request, 'all_documents_page.html', context)
    else:
        context = {"failed" : True}
        return render(request, 'index.html', context)

#image view
def documento5(request, archivo, colección, caja, legajo, carpeta, número_de_imagen):
	
	if request.method == 'POST':
		if request.POST['input'] == 'text_edit':
			edit_form = EditForm(request.POST)
			if edit_form.is_valid():
				print('this is the request',request)
				texto_de_OCR = request.POST['texto_de_OCR']
				file = request.POST.get('nombre_del_archivo', None)
				persona = request.POST.get('persona', None)
				print('here is the persona')
				print(persona)
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

				lugar = request.POST.get('ubicación_geográfica', None)
				actividades_políticas = request.POST.get('actividades_políticas', None)
				fecha_desaparicion = request.POST.get('fecha_desaparicion', None)
				genero = request.POST.get('genero', None)
				manuscritos = request.POST.get('manuscripts', None)
				#save with the new data
				image = Imagen.objects.get(nombre_del_archivo = file)
				image.texto_de_OCR = texto_de_OCR

				try:
					image.persona.add(persona)
				except:
					pass

				try:
					image.ubicación_geográfica.add(lugar)
				except:
					pass

				try:
					image.actividades_políticas.add(actividades_políticas)
				except:
					pass

				image.save() 

				clipboard = PortapapelesForm(request.POST)
				 
				
				state = Imagen.objects.get(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta, número_de_imagen=número_de_imagen)	
				context  = {'state':state, 'form':edit_form, 'clipboard':clipboard}
				return render(request, 'document_page.html', context)
			
			else:
				print(edit_form.errors)

		if request.POST['input'] == 'clipboard':
			clipboard = PortapapelesForm(request.POST)
			if clipboard.is_valid():
				response = dict(clipboard.data)
				choice = response.get('list_name', None)
				print('choice',choice)
				clipboards = Portapapeles.objects.all()
				print('clipboards',clipboards)
				chosen = clipboards[int(choice[0])-1]
				#print(chosen)
				user = response.get('user', None)
				file = response.get('filename', None)
				print ('Clipboard!', dict(clipboard.data))
				user_id = User.objects.get(username=user[0]).pk
				clip = Portapapeles.objects.get(nombre_del_portapapeles=chosen, usuario=user_id)
				clip.imágenes.add(Imagen.objects.get(nombre_del_archivo=file[0]).pk) 
				clip.save()

				state = Imagen.objects.get(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta, número_de_imagen=número_de_imagen)	
				id = state.id
				form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})

				context  = {'state':state,'form':form,'clipboard':clipboard,'id':id}		
				return render(request, 'document_page.html', context)

	else:
		state = Imagen.objects.get(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta, número_de_imagen=número_de_imagen)	
		#TODO add forward + backward buttons
		possible_pages = Imagen.objects.filter(archivo__nombre_del_archivo=state.archivo, colección__nombre_de_la_colección=state.colección, caja=state.caja, legajo=state.legajo, carpeta=state.carpeta).order_by('número_de_imagen')	
		pages_list = []
		for index, page in enumerate(possible_pages):
			pages_list.append(page)

			#print(index, page)
			if page == state:
				print('current= ', page.número_de_imagen, index)
				current = int(index)
		previous = pages_list[current-1].número_de_imagen
		try:
			next_one = pages_list[current+1].número_de_imagen
		except:
			next_one = pages_list[0].número_de_imagen

		print('previous= ', previous)
		print('next= ', next_one)
		#next_one = pages_list[int(current)+1]
		#print(current, next_one, previous)
			#print(index, page)
			#if page == state:
			#	print('this is it', page.número_de_imagen, index)
		#		current = index
		#	next_one = current + 1, page
		#	print(next_one) 
			#print (possible_pages)

		id = state.id
		form = EditForm(initial={'texto_de_OCR':state.texto_de_OCR})
		clipboard = PortapapelesForm(request.POST)
		context  = {'state':state, 'form':form, 'clipboard':clipboard, 'id':id, 'previous':previous, 'next_one':next_one}		
		return render(request, 'document_page.html', context)

#carpeta view
def documento4(request, archivo, colección, caja, legajo, carpeta):

	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo, carpeta=carpeta).order_by('número_de_imagen')	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja, 'legajo':legajo, 'carpeta':carpeta}
	possible_carpeta = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo).order_by('carpeta')	
	carpeta_list = []
	#make a list of the possible carpetas with index values
	for index, page in enumerate(possible_carpeta):
		if page.carpeta not in carpeta_list:
			carpeta_list.append(page.carpeta)
	for item in carpeta_list:
		if item == carpeta:
			current = item
			print('current is',current)
	#find index in list for current
	index_current= carpeta_list.index(current)
	previous_carpeta = carpeta_list[index_current-1]
	try:
		next_carpeta = carpeta_list[index_current+1]
	except:
		next_carpeta = carpeta_list[0]
	carpeta_info = Caso.objects.filter(caja_no=caja, legajo_no=legajo, carpeta_no=carpeta)

	context = {'state':state, 'location':location, 'previous_carpeta':previous_carpeta, 'next_carpeta':next_carpeta, 'carpeta_info':carpeta_info}
	return render(request, 'all_documents_page.html', context)

#legajo view
def documento3(request, archivo, colección, caja, legajo):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja, legajo=legajo).order_by('carpeta')	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja, 'legajo':legajo}
	possible_legajo = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja).order_by('legajo')
	legajo_list = []
	#make a list of the possible carpetas with index values
	for index, page in enumerate(possible_legajo):
		if page.legajo not in legajo_list:
			legajo_list.append(page.legajo)
	for item in legajo_list:
		if item == legajo:
			current = item
	print(legajo_list, current, legajo_list.index(current))
		
	#find index in list for current
	index_current= legajo_list.index(current)
	previous_legajo = legajo_list[index_current-1]
	try:
		next_legajo = legajo_list[index_current+1]
		print(next_legajo)
	except:
		next_legajo = legajo_list[0]
		print(next_legajo)
	context = {'state':state, 'location':location, 'previous_legajo':previous_legajo, 'next_legajo':next_legajo}
	return render(request, 'all_documents_page.html', context)

def documento2(request, archivo, colección, caja):
	
	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección, caja=caja).order_by('legajo')	
	location = {'archivo':archivo, 'colección':colección, 'caja':caja}
	possible_caja = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección).order_by('caja')
	caja_list = []
	#make a list of the possible carpetas with index values
	for index, page in enumerate(possible_caja):
		if page.caja not in caja_list:
			caja_list.append(page.caja)
	for item in caja_list:
		if item == caja:
			current = item
		else:
			current = caja_list[0]
	#find index in list for current
	index_current= caja_list.index(current)
	previous_caja = caja_list[index_current-1]
	try:
		next_caja = caja_list[index_current+1]
	except:
		next_caja = caja_list[0]
	context = {'state':state, 'location':location, 'previous_caja':previous_caja, 'next_caja':next_caja}
	return render(request, 'all_documents_page.html', context)

def documento1(request, archivo, colección):
	

	state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo, colección__nombre_de_la_colección=colección).order_by('caja')	
	location = {'archivo':archivo, 'colección':colección}
	context = {'state':state, 'location':location}
	return render(request, 'all_documents_page.html', context)

@login_required
def documento0(request, archivo):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		query = request.POST.get('search', None)
		if form.is_valid():
			state = Imagen.objects.filter(texto_de_OCR__icontains=query).order_by('colección')
			context  = {'state':state, 'form':form}
			return render(request, 'all_documents_page.html', context)
		else:
			print(form.errors)
	else:
		search = ""
		form = SearchForm(initial={'search': search })
		state = Imagen.objects.filter(archivo__nombre_del_archivo=archivo).order_by('número_de_imagen')
		location = {'archivo':archivo}
		context = {'state':state,'form':form, 'location':location }
		
		return render(request, 'all_documents_page.html', context)



		
