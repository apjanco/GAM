import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Caso, Persona


class Command(BaseCommand):
    help = "Importa personas de los títulos de Casos"

    def handle(self, *args, **options):
        print("**Importar personas a Django**")
        for e in Caso.objects.all():
            Persona.objects.update_or_create(nombre_de_la_persona=e.caso)
