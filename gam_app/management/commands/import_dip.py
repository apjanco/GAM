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
from shutil import copyfile
import pyvips
from archivo.settings_secret import API_KEY
import re
from pathlib import Path


class CurrentItem:
    """An object to hold the current bag and letters values. Values are written
    by the first image with a particular letter pattern (a, bbb, cc).  As the script moves 
    down the list, later occurances of that pattern are written to the initial item.  
    This prevents the creation of multiple items for a given letter pattern."""

    def __init__(self, name, letters):
        self.name = name
        self.letters = letters

def clean_dzis():
    """This function fixes a peculiarity of the dzi making process for openseadragon.
    """
    files = os.listdir('/mnt/dzis1/')
    for file in files:
        try:
            if 'jpg' in file:
                continue

            elif 'files' in file:
                front = file[:-6] + '.jpg_files'
                check_existing = Path('/mnt/dzis1/{}'.format(front))
                if check_existing.exists():
                    continue
                else:
                    os.rename('/mnt/dzis1/{}'.format(file), '/mnt/dzis1/{}'.format(front))

            else:
                new = file[:-3] + 'jpg.dzi'
                os.rename('/mnt/dzis1/{}'.format(file), '/mnt/dzis1/{}'.format(new))
        except:
            print('exception')



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
        directory = '/tmp/DIP/' + dip_name + '/objects/'
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
                        try:
                            text = response['responses'][0]['textAnnotations'][0]['description']
                            text = text.encode('utf-8')
                        except:
                            text = ''
                            text = text.encode('utf-8')
                        #TODO write entire response to MongoDB
                        return text 

def reformat_old_bag(dip_name):
    """This is a function for re-importing bags that were created before the filenames were changed to include the archive and collection names."""
    for file in os.listdir('/tmp/DIP/' + dip_name + '/objects/'):
        filename = file.split('-')[-1]
        filename = 'gam_des_' + filename
        uuid = file.split('-')[:-1]
        uuid = '-'.join(uuid)
        rejoined = uuid + '-' + filename
        os.rename('/tmp/DIP/{}/objects/{}'.format(dip_name, file), '/tmp/DIP/{}/objects/{}'.format(dip_name, rejoined))

class Command(BaseCommand):
        help = "Imports data from an Archivematica DIP in tmp/DIP into the database"
        def handle(self, *args, **options):
                print ("**Import DIP to Django**")
                current_item = CurrentItem
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
                        #skip the csv file made for DIP upload
                        #if file.split('.')[1] == 'txt':
                        #    resumenes = file.read()
                        if file.split('.')[1] != 'jpg' or 'txt':
                                pass
                        
                        if file.split('.')[1] == 'jpg':
                            path = '/tmp/DIP/' + dip_name + '/objects/' + file
                            #change to 4mb if larger
                            change_size_if_needed(path)
                            
                            # remove uuid
                            location = file.split('-')[-1]
                            # remove .jpg
                            location = location.split('.')[0]
                            physical_location = location
                            #print(physical_location)
                            #print(location)
                            parts = location.split('_')
                            #print(parts)
                            archive = parts[0].lower()
                            collection = parts[1].lower()
                            box = parts[2]
                            bundle = parts[3]
                            try:
                               folder = parts[4]
                            except IndexError:
                                reformat_old_bag(dip_name)
                                continue
                            image = parts[5]

                            if archive == 'gam':
                                archivo_id = Archivo.objects.get(nombre_del_archivo='Archivo del GAM')
                            else:
                                archivo_name = input("That archive does not exist, please enter a new archive name: ")
                                Archivo.objects.get_or_create(nombre_del_archivo= archivo_name)
                                archivo_id = Archivo.objects.get(nombre_del_archivo='%s' % archivo_name)
                            
                            if collection == 'des':
                                #print(collection)
                                collection_id = Colección.objects.get(nombre_de_la_colección='Desaparecidos')

                            elif collection == 'nin':
                                collection_id = Colección.objects.get(nombre_de_la_colección='Niñez Desparecida')

                            else:
                                collection_name = input("That collection does not exist, please enter a new collection name: ")
                                Colección.objects.get_or_create(nombre_de_la_colección=collection_name)
                                collection_id = Colección.objects.get(nombre_de_la_colección='%s' % collection_name)
                            
                            #create the document in the db
                            Imagen.objects.update_or_create(
                                nombre_del_archivo= file,
	                        localizacion_fisica = physical_location,
        	                archivo_id = archivo_id.pk,
                	        colección_id = collection_id.pk,
                                caja = box,
                                legajo = bundle,
                                carpeta = folder,
                                número_de_imagen = image,
                                #texto_de_OCR = ocr_text,
                                bag_name = dip_name,
                                #defaults = {'caja': box, 'legajo': bundle, 'archivo_id': archivo_id.pk, 'colección_id': collection_id.pk, 'carpeta': folder, 'número_de_imagen': image, 'texto_de_OCR': ocr_text, }
                            )

                            #move jpg files to static
                            #https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
                            #https://boto3.readthedocs.io/en/latest/guide/migrations3.html#storing-data
                            #s3.Object('archivo', file).put(Body=open(path, 'rb'))
                            copyfile(path, '/mnt/documents/%s' % file)
                            #copyfile(path, '/mnt/dzis/documents/%s' % file)
                            #move thumbnail to static folder
                            parts = file.split('-')[:-1]
                            uuid = ''
                            for i in parts:
                                uuid += i + '-'
                            #print(uuid[:-1])
                            thumbnail = '/tmp/DIP/' + dip_name + '/thumbnails/' + uuid[:-1] + '.jpg'

                            copyfile(thumbnail,'/mnt/thumbnails/%s' % file)

                            #create dzis for Openseadragon and move to static
                            try:
                                #print('path is: %s' % path)
                                print('[*] %s' % file)
                                dzi_me = pyvips.Image.new_from_file(path)
                                dzi_me.dzsave('/mnt/dzis1/%s' % file) 
                                #subprocess.call('mv /srv/GAM/gam_app/dzis/%s.dzi /srv/GAM/gam_app/dzis/%s.dzi' % (file.split('.')[0], file))
                                #subprocess.call('mv /srv/GAM/gam_app/dzis/%s_files /srv/GAM/gam_app/dzis/%s_files' %  (file.split('.')[0], file))
                            except Exception as e:
                                print(e)
                            
                        #  Read the folder descriptions and write them to a folder object
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
                               
                               if re.search('^\w{3}_\w{3}_\d{3}', content[i]):
                                   keys.append(i)
                           
                           for i in range(len(keys)):
                               try:
                                   carpeta_descripcion[content[keys[i]]] = content[(keys[i]+1):keys[i+1]]
                               except IndexError:
                                   carpeta_descripcion[content[keys[i]]] = content[(keys[i]+1):]

                           #print(carpeta_descripcion)
                           for carpeta in carpeta_descripcion:
                               print('[*]', carpeta)
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
                               elif collection == 'nin':
                                   collection_id = Colección.objects.get(nombre_de_la_colección='Niñez Desparecida')

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
                
                clean_dzis()

                # create items for all of the images in the DIP
                bag = dip_name
                bags = {}
                bags[bag] = {}
                query_imagens = Imagen.objects.filter(
                    bag_name=bag).order_by(
                    "caja", "legajo", "carpeta", "número_de_imagen")

                #  create a list from the queryset that will allow indexing
                imagens_list = []
                for item in query_imagens:
                    imagens_list.append(item.nombre_del_archivo)

                for index, image in enumerate(imagens_list):
                    número_de_imagen = image.split('.')[0]
                    número_de_imagen = número_de_imagen.split('_')[-1]

                    # file number has letter
                    if re.search('[a-zA-Z]', número_de_imagen):
                        letters = ''.join(
                            [i for i in número_de_imagen if not i.isdigit()])

                        #  check previous image, if previous had no letters
                        if letters not in imagens_list[index-1].split(
                            '.')[0].split('_')[-1]:

                            #  create an item from physical
                            #  location minus letters
                            item_name = image.split('.')[0].split(
                                '-')[-1][:-len(letters)]
                            bags[bag][item_name] = []

                            #  add current image to the item
                            bags[bag][item_name].append(image)

                            #  variable to hold current item name
                            current_item.name = item_name
                            current_item.letters = letters

                        #  if previous had letters, add to existing item
                        elif current_item.letters in imagens_list[index-1].split('.')[0].split('_')[-1]:
                            try:
                                bags[bag][current_item.name].append(image)

                            except:
                                print('[*] Error with {}'.format(
                                    current_item.name))
                                continue

                    # file number has no letters : create single-image item
                    else:
                        bags[bag][image.split('.')[0].split('-')[-1]] = []
                        bags[bag][image.split('.')[0].split('-')[-1]].append(image)

                    for key, value in bags.items():
                        for value1 in value.items():
                        # get item with name in the list
                            try:
                                item = Item.objects.get(nombre_del_item=value1[0])
                            except:
                                item = Item(nombre_del_item=value1[0])
                                item.save()

                            for file in value1[1]:
                                image = Imagen.objects.get(nombre_del_archivo=file)
                                image.item = item
                                image.save()


