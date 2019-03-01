from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from gam_app.models import *
from acceso.models import *
from gam_app.models import Persona


def main(request):
    casos = Caso.objects.all()
    photo_list = []
    for caso in casos:
        photo_list.append(caso.fotos.first())

    #print('casos:  ', casos)
    context = {'casos': casos, 'photo_list': photo_list}
    return render(request, 'acceso/index.html', context)


def about(request):
    return render(request, 'acceso/about.html', {})

def network(request):
    return render(request, 'acceso/bestsellers_graph.html',)

def map(request):
    return render(request, 'acceso/map.html', {})


def history(request):
    return render(request, 'acceso/history.html', {})


def caso(request, caso):
    caso = Caso.objects.get(slug_name=caso)
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

    persona = Persona.objects.get(nombre_de_la_persona=caso)
    temp = persona.__dict__
    persona_dict = {
        k.replace("_", " ").capitalize(): v for k, v in temp.items() if len(str(v)) > 0
    }
    for x in caso.fotos.all():
        foto.append(x)
    persona_dict = {
        key: persona_dict[key] for key in persona_dict if key not in ["Id", " state"]
    }
    keys = []
    values = []
    for i in sorted(persona_dict.keys()):
        keys.append(i)
        values.append(persona_dict[i])
    kv = zip(keys, values)
    profile_photos = Foto.objects.filter(caso__slug_name=caso)
    context = {'caso': caso, 'images': foto, "kv": kv, 'dragon': dragon, 'face':imageprofile}

    return render(request, 'acceso/caso.html', context)


def simple(request):
    casos = Caso.objects.all()
    context = {'casos': casos}
    return render(request, 'simple/acceso.html', context)


def caso_index(request):
    return render(request, 'acceso/caso_index.html')


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
