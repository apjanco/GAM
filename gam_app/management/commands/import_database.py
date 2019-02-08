import csv
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Caso


class Command(BaseCommand):
    help = "Importa datos de la base de datos GAM de Google Drive desde csv"

    def handle(self, *args, **options):
        print("**Importar base de datos a Django**")

        with open('/tmp/gam-loading-data1.csv') as f:
            for row in csv.DictReader(f, skipinitialspace=True):
                print(row)
                Caso.objects.update_or_create(
                    caso=row['Caso'],
                    fecha_desaparicion=row['fecha_desaparicion'][:10],
                    departamento=row['departamento'],
                    local=row['local'],
                    area=row['area'],
                    ambiente=row['ambiente'],
                    estanteria_no=row['estanteria_no'],
                    plato_no=row['plato_no'],
                    caja_no=row['caja_no'],
                    legajo_no=row['legajo_no'],
                    carpeta_no=row['carpeta no'],
                    descripcion_caso=row['descripcion_caso'],
                )
