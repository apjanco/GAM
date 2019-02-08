import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen


class Command(BaseCommand):
        help = "Importa datos de la base de datos GAM de Google Drive desde csv"
        def handle(self, *args, **options):
                print ("**Importar base de datos a Django**")
                
                with open('/tmp/vision_ocr1.csv') as f:
                    for row in csv.DictReader(f, skipinitialspace=True):
                        try:
                        print(row)
                        filename = row['filename']
                        text = row['text']

                        #image = Imagen.objects.get(nombre_del_archivo=filename)
                        #image.notas = text
                        #image.save


                        
