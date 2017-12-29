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
from PIL import Image
#import boto3
#s3 = boto3.resource('s3')
from shutil import copyfile
from gam_app.settings_secret import API_KEY


#ocr_text = 'testing ocr test'
#This section changes the size of an image file if it is larger than 4MB
#https://stackoverflow.com/questions/13407717/python-image-library-pil-how-to-compress-image-into-desired-file-size
class file_counter(object):
    def __init__(self):
        self.position = self.size = 0

    def seek(self, offset, whence=0):
        if whence == 1:
            offset += self.position
        elif whence == 2:
            offset += self.size
        self.position = min(offset, self.size)

    def tell(self):
        return self.position

    def write(self, string):
        self.position += len(string)
        self.size = max(self.size, self.position)

def smaller_than(im, size, guess=70, subsampling=1, low=1, high=100):
    while low < high:
        counter = file_counter()
        im.save(counter, format='JPEG', subsampling=subsampling, quality=guess)
        if counter.size < size:
            low = guess
        else:
            high = guess - 1
        guess = (low + high + 1) // 2
    return low

def change_size_if_needed(file):
    if os.path.getsize(file) > 4000000:
        im = Image.open(file)
        size = smaller_than(im,4000000)
        im.save(file, 'JPEG', quality=size)


def vision_ocr(dip_name,file):
        #TODO

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
                    if project == '.DS_Store':
                        pass
                    else:    
                        print(project_list.index(project), project)
                
                dip = input("Enter the number of the DIP for import: ") 
                #bag_name = raw_input("Enter the name of the DIP for upload: ")
                dip_name = project_list[int(dip)]
                print("Let's import %s" % dip_name) 

                collection_choice = input("Collection -- Enter 1 for desaparecidos, 2 for casos legales: ") 

                if collection_choice == '1':
                    collection = 'desaparecidos'

                elif collection_choice == '2':
                    collection = 'casos_legales'

                else:
                    collection = ''


                for file in os.listdir('/Users/ajanco/projects/GAM/DIPs/' + dip_name + '/objects/'):
                        #skip the csv file made for DIP upload
                        if file.split('.')[1] != 'jpg':
                                pass
                        
                        if file.split('.')[1] == 'jpg':
                            path = '/Users/ajanco/projects/GAM/DIPs/' + dip_name + '/objects/' + file
                            #change to 4mb if larger
                            change_size_if_needed(path)
                            
                            #send to vision for ocr
                            ocr_text = vision_ocr(dip_name,file)
                            print('File: %s' % file)
                            print('Text: %s' % ocr_text.decode('utf-8'))
                            
                            
                            location = file.split('-')[-1]
                            location = location.split('.')[0]
                            physical_location = location
                            #print(physical_location)
                            #print(location)
                            parts = location.split('_')
                            #print(parts)
                            box = parts[0]
                            bundle = parts[1]
                            folder = parts[2]
                            image = parts[3]

                            #url and thumbnail urls (valid after collectstatic)
                            url = 'https://archivo.nyc3.digitaloceanspaces.com/static/documents/' + file
                            thumbnail = 'https://archivo.nyc3.digitaloceanspaces.com/static/thumbnails/' + file

                            #create the document in the db
                            Document.objects.update_or_create(
                            filename = file,
                            physical_location = physical_location,
                            url = url,
                            thumbnail = thumbnail,
                            archivo = 'Archivo del Grupo de Apoyo Mutuo',
                            collection = collection,
                            box = box,
                            bundle = bundle,
                            folder = folder,
                            image = image,
                            ocr_text = ocr_text.decode('utf-8'),
                            )
                            #move jpg files to static
                            #https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
                            #https://boto3.readthedocs.io/en/latest/guide/migrations3.html#storing-data
                            #s3.Object('archivo', file).put(Body=open(path, 'rb'))
                            copyfile(path, '/Users/ajanco/projects/GAM/archivo/gam_app/static/documents/%s' % file)

                            #move thumbnail to static folder
                            parts = file.split('-')[:-1]
                            uuid = ''
                            for i in parts:
                                uuid += i + '-'
                            print(uuid[:-1])
                            thumbnail = '/Users/ajanco/projects/GAM/DIPs/' + dip_name + '/thumbnails/' + uuid[:-1] + '.jpg'

                            copyfile(thumbnail,'/Users/ajanco/projects/GAM/archivo/gam_app/static/thumbnails/%s' % file)
                print('To complete and upload to DO Space, run collectstatic')
                #create DZIs for open sea dragon? 
                #what to do with METs file
                #what is processing MCP file? 



