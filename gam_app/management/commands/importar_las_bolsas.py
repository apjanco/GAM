from django.core.management.base import BaseCommand, CommandError
from gam_app.tracking import *


class Command(BaseCommand):
    help = """Este es un comando que controlará automáticamente los depósitos en el almacenamiento en la nube en busca 
    de nuevas bolsas. Luego validará, descomprimirá e importará las nuevas bolsas."""

    def handle(self, *args, **options):
        bolsas = set(getBags())
        bolsas_importadas = set(getImportedBags())
        bolsas_nuevas = bolsas.difference(bolsas_importadas)

        for bolsa in bolsas_nuevas:

            if descargar_una_sola_bolsa(bolsa + '.zip'):
                 print('descargado {}'.format(bolsa))
                 os.system('rm /tmp/{}'.format(bolsa + '.zip'))

            #if descargar_una_sola_bolsa_s3cmd(bolsa + '.zip'):
            #    print('s3cmd descargado {}'.format(bolsa))
            #    os.system('rm /tmp/{}'.format(bolsa + '.zip'))





