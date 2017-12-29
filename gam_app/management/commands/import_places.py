import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Caso, Place


class Command(BaseCommand):
        help = "Imports places from the Casos titles"
        def handle(self, *args, **options):
                print ("**Import Places to Django**")
                for e in Caso.objects.all():
                    Place.objects.update_or_create(
                            place_name = e.departamento,
                            )
                        
