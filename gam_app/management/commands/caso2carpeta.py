from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *
from django.shortcuts import get_object_or_404


class Command(BaseCommand):
    help = "Turn Casos into Carpetas"

    def handle(self, *args, **options):
        print("**Create Carpeta Summaries**")
        carpetas = Imagen.objects.values(
            'archivo', 'colección', 'caja', 'legajo', 'carpeta'
        ).distinct()
        for carpeta in carpetas:
            archivo = carpeta['archivo']
            colección = carpeta['colección']
            caja = carpeta['caja']
            legajo = carpeta['legajo']
            carpeta = carpeta['carpeta']

            # TODO get all text from images in carpeta
            folders = Caso.objects.filter(
                caja_no=caja, legajo_no=legajo, carpeta_no=carpeta
            )
            print(folders)
            for file in folders:
                Carpeta.objects.update_or_create(
                    archivo=get_object_or_404(Archivo, id=archivo),
                    colección=get_object_or_404(Colección, id=colección),
                    caja=caja,
                    legajo=legajo,
                    carpeta=carpeta,
                    descripción=file.descripcion_caso,
                )
