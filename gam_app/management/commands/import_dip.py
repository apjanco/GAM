import sys
import os
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *
import googleapiclient.discovery
from google.cloud import vision
import base64
import io
import pprint
import shutil
import subprocess


API_KEY = 'AIzaSyBZZcmX_W0rFAJUmHbLnQyOGOxJqdm902w'
ocr_text = 'testing ocr test'



def vision_ocr(dip_name,file):
        #TODO
        #Pre-process file, currently too big for Vision 4MB, currently 6MB

        service = googleapiclient.discovery.build('vision', 'v1', developerKey=API_KEY)
        language = 'es'
        directory = '/Users/ajanco/projects/GAM/DIPs/' + dip_name + '/objects/'
        with open(directory + file, 'rb') as image:
                image_content = base64.b64encode(image.read())
                service_request = service.images().annotate(body={
                        'requests': [{
                                                'image': {
                                               'content': image_content.decode('UTF-8')
                                           },
                                       'imageContext': {
                                           'languageHints': [language]},
                                   'features': [{
                                            'type': 'TEXT_DETECTION'
                                    }]
                                        }]
                })
                response = service_request.execute()

                if 'error' in response['responses'][0]:
                        print('[*] error %s' % file)
                        pass

                else:
                        text = response['responses'][0]['textAnnotations'][0]['description']
                text = text.encode('utf-8')
                return text 


class Command(BaseCommand):
        help = "Imports data from an Archivematica DIP in tmp/DIP into the database"
        def handle(self, *args, **options):
                print ("**Import DIP to Django**")

                project_list = os.listdir('/Users/ajanco/projects/GAM/DIPs/') #change to '/tmp/DIP'

                for project in project_list:
                    print(project_list.index(project), project)
                
                dip = input("Enter the number of the DIP for import: ") 
                #bag_name = raw_input("Enter the name of the DIP for upload: ")
                dip_name = project_list[int(dip)]
                print("Let's import %s" % dip_name) 

                collection_choice = input("Collection -- Enter (1) for desaparecidos, (2) for casos legales: ") 
                if collection_choice == 1:
                    collection = 'desaparecidos'
                if collection_choice == 2:
                    collection = 'casos_legales'
                else:
                    collection = collection_choice

                for file in os.listdir('/Users/ajanco/projects/GAM/DIPs/' + dip_name + '/objects/'):
                        if file.split('.')[1] == 'csv':
                                pass

                        else:
                            ocr_text = vision_ocr(dip_name,file)

                            location = file.split('-')[-1]
                            location, physical_location = location.split('.')[0]
                            location = location.split('_')
                            box = location[0]
                            bundle = location[1]
                            folder = location[2]
                            image = location[3]

                            
                            Document.objects.update_or_create(
                            filename = file,
                            physical_location = physical_location,
                            archivo = 'Archivo del Grupo de Apoyo Mutuo',
                            collection = collection,
                            box = box,
                            bundle = bundle,
                            folder = folder,
                            image = image,
                            ocr_text = ocr_text,
                            )
                            #move jpg to static?
                            #move thumbnail to static?
                            #create DZIs for open sea dragon? 
                            #what to do with METs file
                            #what is processing MCP file? 



