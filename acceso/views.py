from itertools import cycle
from bokeh.embed import server_document
from bokeh.embed import server_session
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from acceso.models import *
from gam_app.models import Persona
from gam_app.models import Caso as Database
import os
import random
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.utils.html import escape
from django.db.models import Count, Q

def cycle(iterable):
    saved = []
    for element in iterable:
        yield element
        saved.append(element)
    while saved:
        for element in saved:
            yield element

def bokeh(request):
    script = server_document(url="https://archivogam.haverford.edu/en/acceso/bokeh/people", relative_urls=True)
    return render(request, 'acceso/bokeh.html', {'script': script})
	

def random_photo():
    #yield from cycle(os.listdir('/srv/GAM/acceso/static/pat_goudvis'))
    photos = os.listdir('/srv/GAM/acceso/static/pat_goudvis')
    photo = random.choice(photos)
    return photo

def next_photo():
        photos = os.listdir('/srv/GAM/acceso/static/pat_goudvis')
        num = 0
        while num < len(photos)-1:
            yield photos[num]
            num += 1

def main(request, options):
    casos = Caso.objects.all()
    filters = Filtros.objects.all()
    filter_list = []
    for filter in filters:
        filter_list.append(filter.nombre_del_filtro)
    photo_list = []
    for caso in casos:
        photo_list.append(caso.fotos.first())

    photo = random_photo()
    #photos = os.listdir('/srv/GAM/acceso/static/pat_goudvis')
    #photo = cycle(photos)
    #photo = next(photo)
    #print(photo)
    #print('casos:  ', casos)
    context = {'casos': casos, 'photo_list': photo_list, 'filter_list':filter_list, 'photo': photo}

    return render(request, 'acceso/index.html', context)

def filtrar_imagenes(request):
    filter_list = ["", "none"] #Don't know how to add filters since images models are being created dynamically
    photo = random_photo()
    photo_list = []
    for image in os.listdir('/srv/GAM/acceso/static/diario_militar/thumbnails')[:10]:
        foto = Photo(file=image, folder=image[38:-11])
        photo_list.append(foto)
    context = {'photo_list':photo_list, 'filter_list': filter_list, 'photo':photo}
    return render(request, 'acceso/filtrar_imagenes.html', context)

def skynet(request):
    photo = [[532, "dataset/cat/2008_007496.jpg", 0.4442075490951538],
             [548, 'dataset/cat/2008_003622.jpg', 0.46999311447143555],
             [530, 'dataset/cat/2008_006999.jpg', 0.471227765083313],
             [543, 'dataset/cat/2008_005252.jpg', 0.4816729426383972],
             [517, 'dataset/cat/2008_004303.jpg', 0.4869983196258545],
             [508, 'dataset/cat/2008_001885.jpg', 0.49179962277412415],
             [541, 'dataset/cat/2008_005386.jpg', 0.4957163631916046],
             [509, 'dataset/cat/2008_000182.jpg', 0.4999980032444],
             [527, 'dataset/cat/2008_000345.jpg', 0.5011175274848938],
             [545, 'dataset/cat/2008_001335.jpg', 0.5041385889053345]]
    n = 0
    photoclean = []
    for i in photo:
        photoclean.append(i[1])
    print(photoclean)

    return render(request, 'acceso/skynet.html', {'photo':photoclean})

def about(request):
    photo = random_photo()
    return render(request, 'acceso/about.html', {'photo':photo})

def network(request):
    return render(request, 'acceso/bestsellers_graph.html',)

def collection(request):
    photo = random_photo()
    return render(request, 'acceso/collection.html', {'photo':photo, })

def documentos(request):
    casos = Caso.objects.all()
    carpetas = [caso.carpetas.all() for caso in casos]
    all_carpetas = []
    for list_ in carpetas:
        for carpeta in list_:
            all_carpetas.append(carpeta)
    imagens = []
    for i, carpeta in enumerate(carpetas):
        images = Imagen.objects.filter(
            archivo=all_carpetas[i].archivo,
            colección=all_carpetas[i].colección,
            caja=all_carpetas[i].caja,
            legajo=all_carpetas[i].legajo,
            carpeta=all_carpetas[i].carpeta,
        ).order_by('número_de_imagen')
        imagens.append(images)
    imagen_names = []
    for image in imagens:
        for imagen in image:
            imagen_names.append(imagen.nombre_del_archivo)
    return render(request, 'acceso/documentos.html', {'state':imagen_names, })


def history(request):
    photo = random_photo()
    return render(request, 'acceso/history.html', {'photo':photo})


def caso(request, caso):
    caso = Caso.objects.get(slug_name=caso)
    #caso = CasoFilter(request.GET, queryset=Caso.objects.get(slug_name=caso))
    foto = []
    dragon = []
    imageprofile = caso.foto_de_perfil


    for x in caso.carpetas.all():
        dragon = Imagen.objects.filter(
            archivo=x.archivo,
            colección=x.colección,
            caja=x.caja,
            legajo=x.legajo,
            carpeta=x.carpeta,
        ).order_by('número_de_imagen')
    personas = caso.personas.all()
    # iterate through personas to make a table of all people
    #info = [persona.nombre_de_la_persona, persona.nombre, persona.segundo, persona.apellido_paterno, persona.apellido_materno, persona.fecha_de_nacimiento, persona.fecha_desaparicion, persona.edad_en_el_momento, persona.género, persona.etnicidad, persona.profesión, persona.actividades_políticas]
    #if str(info[-1]) == "gam_app.Organización.None":
    #    info[-1] = ""
    for x in caso.fotos.all():
        foto.append(x)
    profile_photos = Foto.objects.filter(caso__slug_name=caso)
    context = {'caso': caso, 'images': foto,'personas':personas, 'dragon': dragon, 'face':imageprofile}

    return render(request, 'acceso/caso.html', context)


def simple(request):
    casos = Caso.objects.all()
    context = {'casos': casos}
    return render(request, 'simple/acceso.html', context)


def caso_index(request):
    return render(request, 'acceso/caso_index.html')

def datatable(request):
    return render(request, 'acceso/datatable.html')

def caso_table(request, caso_id):
    # TODO: Probably want nombre_del_caso to be an explicit part of the URL rather than
    # a GET parameter.
    caso = Caso.objects \
        .filter(nombre_del_caso__icontains=request.GET.get('nombre_del_caso')) \
        .filter(descripción__icontains=request.GET.get('descripción'))
    return JsonResponse(serializers.serialize(caso))

def network_json(request):

    """{
      "nodes":[
            {"name":"node1","group":1},
            {"name":"node2","group":2},
            {"name":"node3","group":2},
            {"name":"node4","group":3}
        ],
        "links":[
            {"source":2,"target":1,"weight":1},
            {"source":0,"target":2,"weight":3}
        ]
    }"""

    dict = {'nodes': [], 'links': []}
    with open('/srv/GAM/acceso/my_file.txt', 'r') as f:
        node_list = list([line.split(',')[0] for line in f])
        for node in set(node_list):
            dict['nodes'].append({"name": node, "group": 1}, )

    with open('/srv/GAM/acceso/my_file.txt', 'r') as f: 
        for line in f:
            node = line.split(',')[0]
            target = line.split(',')[1]
            weight = line.replace('\n', '').split(',')[2]
            if weight != "0.0":
                node_index = dict['nodes'].index({"name":node, "group":1},)
                try:
                    target_index = dict['nodes'].index({"name": target,"group":1},)
                except:
                    pass
                dict['links'].append({"source": node_index, "target": target_index, "weight": float(weight) * 10})



        response = JsonResponse(dict)
        return response
      
class DbListJson(BaseDatatableView):
    # the model you're going to show
    model = Database

    # define columns that will be returned
    # they should be the fields of your model, and you may customize their displaying contents in render_column()
    # don't worry if your headers are not the same as your field names, you will define the headers in your template
    columns = ['caso', 'fecha_desaparicion', 'departamento','descripcion_caso', ]

    # define column names that will be used in sorting
    # order is important and should be same as order of columns displayed by datatables
    # for non sortable columns use empty value like ''
    order_columns = ['caso', 'fecha_desaparicion', 'departamento','descripcion_caso', ]

    # set max limit of records returned
    # this is used to protect your site if someone tries to attack your site and make it return huge amount of data
    max_display_length = 500

    def render_column(self, row, column):

        return super(DbListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # here is a simple example
        search = self.request.GET.get('search[value]', None)
        if search:
            q = Q(caso__icontains=search) | Q(descripcion_caso__icontains=search) | Q(fecha_desaparicion__icontains=search) | Q(departamento__icontains=search)
            qs = qs.filter(q)
        return qs

