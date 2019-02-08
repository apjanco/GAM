from gam_app.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        images = Imagen.objects.all()

        for image in images:
            new_caja = Caja.objects.update_or_create(
                archivo=image.archivo,
                colección=image.colección,
                número_de_caja=image.caja,
            )

        carpetas = Carpeta.objects.filter(
            archivo=image.archivo, colección=image.colección, caja=image.caja
        )
        for carpeta in carpetas:
            new_caja.carpetas.add(carpeta)
        new_caja.save()
