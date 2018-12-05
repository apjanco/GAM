import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *


class Command(BaseCommand):
    help = "A little script for moving transcriptions"

    def handle(self, *args, **options):
        images = Imagen.objects.filter(bag_name='jul04_2018_bag33')
        for image in images:
            new = Imagen.objects.get(nombre_del_archivo=image)
            print(new)
            ole = new.nombre_del_archivo.replace('gam_des_', '')
            print(ole)
            old_image = Imagen.objects.get(nombre_del_archivo=ole)
            print(old_image.texto_de_OCR)
            new.texto_de_OCR = old_image.texto_de_OCR
            new.save()
