import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Caso, Person


class Command(BaseCommand):
        help = "Imports people from the Casos titles"
        def handle(self, *args, **options):
                print ("**Import People to Django**")
                state = Caso.objects.all()
                for item in state:
                    Person.objects.update_or_create(
                            person_name = item,
                            )
                        
