import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *


class Command(BaseCommand):
    help = "A little script for checking things before deleting old files"

    def handle(self, *args, **options):
        images = Imagen.objects.all()
        older = []
        for image in images:
            if 'gam_des' not in image.localizacion_fisica:
                if 'gam_nin' not in image.localizacion_fisica:
                    older.append(image.localizacion_fisica)
        print('no. older is ', len(older))

        for image in images:
            checked = []
            old_name = image.localizacion_fisica.replace('gam_des_', '')
            if old_name in older:
                checked.append(old_name)
        print('no checked is ', len(checked))
