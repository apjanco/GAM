import csv
import os
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *


class Command(BaseCommand):
        help = "Check that all image records in the database have a coresponding dzi file"
        def handle(self, *args, **options):
            images = Imagen.objects.all()
            db_records = []
            for image in images:
                db_records.append(image.nombre_del_archivo + '.dzi')
            files = []
                #print(image.nombre_del_archivo)
            for file in os.listdir('/mnt/dzis'):
                if '.dzi' in file:
                    files.append(file)
                else:
                    continue

            #files with no db record
            with open('/tmp/file_no_db.txt', 'w') as nodb:
                for file in files:
                    if file in db_records:
                        continue
                    else:
                        nodb.write(file + '\n')

            #db entries with no files
            with open('/tmp/db_no_file.txt', 'w') as dbnof:
                for record in db_records:
                    if record in files:
                        continue
                    else:
                        dbnof.write(record)
