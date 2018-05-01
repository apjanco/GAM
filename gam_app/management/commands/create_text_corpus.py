from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen 


class Command(BaseCommand):
        help = "Importa datos de la base de datos GAM de Google Drive desde csv"
        def handle(self, *args, **options):
                print ("**Importar base de datos a Django**")
                
                images = Imagen.objects.all()
                text = ''
                for image in images:
                     text += image.texto_de_OCR

                with open('/tmp/gam_text.txt') as f:
                        f.write(text)
                        f.save()