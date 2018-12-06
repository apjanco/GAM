import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Caso, Lugar


class Command(BaseCommand):
    help = "Importa lugares de los títulos de Casos"

    def handle(self, *args, **options):
        print("**Importar lugares a Django**")
        for e in Caso.objects.all():
            Lugar.objects.update_or_create(nombre_del_lugar=e.departamento)
