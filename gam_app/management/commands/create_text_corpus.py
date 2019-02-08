import html
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen
from django.utils.html import strip_tags


class Command(BaseCommand):
    help = "This will save all of the image transcriptions to a txt file"

    def handle(self, *args, **options):
        print("**Transcription2txt**")

        images = Imagen.objects.all()
        text = ''
        for image in images:
            text += strip_tags(html.unescape(image.texto_de_OCR))

        with open('/tmp/gam_text.txt', 'w') as f:
            f.write(text)
