import sys
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *
import io
import pprint
import shutil
import subprocess
from PIL import Image
from shutil import copyfile
from archivo.settings_secret import API_KEY
import re
from pathlib import Path



class Command(BaseCommand):
        help = "Imports data from an Archivematica DIP in tmp/DIP into the database"
        def handle(self, *args, **options):
                print ("**Import DIP to Django**")
                project_list = os.listdir('/tmp/DIP/') #change to '/tmp/DIP'

                for project in project_list:
                    if project == '.DS_Store':
                        pass
                    else:    
                        print(project_list.index(project), project)
                
                dip = input("Enter the number of the DIP for import: ") 
                #bag_name = raw_input("Enter the name of the DIP for upload: ")
                dip_name = project_list[int(dip)]
                print("Let's import %s" % dip_name)

                for file in os.listdir('/tmp/DIP/' + dip_name + '/objects/'):
                       if file.split('.')[1] == 'txt':
                           path = '/tmp/DIP/' + dip_name + '/objects/' + file
                           with open(path, encoding='ISO-8859-1') as fp:
                               content = fp.readlines()
                               content = [x.strip() for x in content]

                           # Gets rid of empty strings (white spaces in this case) from the list  
                           while '' in content:
                               content.remove('')
                           # Dictionary containing bag name as key and bag date and description as value
                           carpeta_descripcion = {}
                           keys = []
                           for i in range(len(content)):
                               if re.search('^gam_', content[i]):
                                   keys.append(i)
                           
                           for i in range(len(keys)):
                               try:
                                   carpeta_descripcion[content[keys[i]]] = content[(keys[i]+1):keys[i+1]]
                               except IndexError:
                                   carpeta_descripcion[content[keys[i]]] = content[(keys[i]+1):]

                           #print(carpeta_descripcion)
                           for carpeta in carpeta_descripcion:
                               print(carpeta, "***")
                               parts = carpeta.split('_')
                               archive = parts[0].lower()
                               collection = parts[1].lower()
                               box = parts[2]
                               bundle = parts[3]
                               folder = parts[4]
                               descripción = carpeta_descripcion[carpeta]
                               descripción = '\n'.join(descripción)
                               
                               if archive == 'gam':
                                   archivo_id = Archivo.objects.get(nombre_del_archivo='Archivo del GAM')
                               else:
                                   archivo_name = input("That archive does not exist, please enter a new archive name: ")
                                   Archivo.objects.get_or_create(nombre_del_archivo= archivo_name)
                                   archivo_id = Archivo.objects.get(nombre_del_archivo='%s' % archivo_name)

                               if collection == 'des':
                                   collection_id = Colección.objects.get(nombre_de_la_colección='Desaparecidos')

                               else:
                                   archivo_name = input("That collection does not exist, please enter a new archive name: ")
                                   Colección.objects.get_or_create(nombre_de_la_colección= collection)
                                   collection_id = Colección.objects.get(nombre_de_la_colección='%s' % collection)

                               Carpeta.objects.update_or_create(
                                    archivo_id = archivo_id.pk,
                                    colección_id = collection_id.pk,
                                    caja = box,
                                    legajo = bundle,
                                    carpeta = folder,
                                    descripción = descripción
                               )
                #what to do with METs file
                #what is processing MCP file? 


