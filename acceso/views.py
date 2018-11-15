from django.shortcuts import render
from acceso.models import *


# Create your views here.
def main(request):
    casos = Caso.objects.all()
    photo_list = []
    for caso in casos:
        photo_list.append(caso.fotos.first())

    print('casos:  ', casos)
    context = {'casos': casos, 'photo_list':photo_list }
    return render(request, 'acceso/index.html', context)


def about(request):
    return render(request, 'acceso/about.html', {})


def map(request):
    return render(request, 'acceso/map.html', {})


def history(request):
    return render(request, 'acceso/history.html', {})


def caso(request, caso):
    caso = Caso.objects.get(slug_name=caso)

    context = {'caso': caso}
    return render(request, 'simple/caso.html', context)


def simple(request):
    casos = Caso.objects.all()
    context = {'casos': casos,}
    return render(request, 'simple/acceso.html', context)









