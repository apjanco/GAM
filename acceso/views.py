from django.shortcuts import render
from gam_app.models import *
from acceso.models import *


# Create your views here.


def main(request):
    casos = Caso.objects.all()
    photo_list = []
    for caso in casos:
        photo_list.append(caso.fotos.first())

    print('casos:  ', casos)
    context = {'casos': casos, 'photo_list': photo_list}
    return render(request, 'acceso/index.html', context)


def about(request):
    return render(request, 'acceso/about.html', {})


def map(request):
    return render(request, 'acceso/map.html', {})


def history(request):
    return render(request, 'acceso/history.html', {})


def caso(request, caso):
    caso = Caso.objects.get(slug_name=caso)
    foto = []
    dragon= []

    for x in caso.fotos.all():
        print(x)
        foto.append(x)



    for x in caso.carpetas.all():
        dragon= Imagen.objects.filter(archivo=x.archivo, colección=x.colección, caja=x.caja,legajo=x.legajo, carpeta=x.carpeta).order_by('número_de_imagen')


    profile_photos = Foto.objects.filter(caso__slug_name=caso)
    
    context = {'caso': caso, 'images': foto, 'dragon':dragon}
    return render(request, 'acceso/caso.html', context)


def simple(request):
    casos = Caso.objects.all()
    context = {'casos': casos,}
    return render(request, 'simple/acceso.html', context)









