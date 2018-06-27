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




def clean_dzis():
    '''This function fixes a peculiarity of the dzi making process for openseadragon.
    '''
    files = os.listdir('/srv/GAM/gam_app/dzis')
    for file in files:
        try:
            if 'jpg' in file:
                continue

            elif 'files' in file:
                front = file[:-6] + '.jpg_files'
                check_existing = Path('/srv/GAM/gam_app/dzis/{}'.format(front))
                if check_existing.exists():
                    continue
                else:
                    os.rename('/srv/GAM/gam_app/dzis/{}'.format(file), '/srv/GAM/gam_app/dzis/{}'.format(front))

            else:
                new = file[:-3] + 'jpg.dzi'
                os.rename('/srv/GAM/gam_app/dzis/{}'.format(file), '/srv/GAM/gam_app/dzis/{}'.format(new))
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
                        #skip the csv file made for DIP upload
                        #if file.split('.')[1] == 'txt':
                        #    resumenes = file.read()
                        if file.split('.')[1] != 'jpg':
                                pass
                        
                        if file.split('.')[1] == 'jpg':
                            path = '/tmp/DIP/' + dip_name + '/objects/' + file
                            #change to 4mb if larger
                            change_size_if_needed(path)

                            

                
                            #send to vision for ocr
                            #try:
                            #    ocr_text = vision_ocr(dip_name,file)
                            #except:
                            #    pass

                            #if ocr_text == None:
                            #    ocr_text = ''
                            #else:
                            #    ocr_text.decode('utf-8')
                            ocr_text = ''
                            #print('File: %s' % file)
                            #print('Text: %s' % ocr_text.decode('utf8'))
                            
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
                            folder = parts[4]
                            image = parts[5]

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
                            print('I am at line 168')
                            print('localizacion_fisica= ',physical_location)
                            print('archivo= ',archivo_id.nombre_del_archivo)
                            print('colección= ', collection_id.nombre_de_la_colección)
                            print('caja= ', box)
                            print('legajo= ', bundle)
                            print('carpeta= ', folder)
                            print('image= ', image)

                            #if not already in db, create a folder entry (carpeta)
                            Carpeta.objects.update_or_create(
                                archivo_id = archivo_id.pk,
                                colección_id = collection_id.pk,
                                caja = box,
                                legajo = bundle,
                                carpeta = folder,
                            ) 


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
                                texto_de_OCR = ocr_text,
                                #defaults = {'caja': box, 'legajo': bundle, 'archivo_id': archivo_id.pk, 'colección_id': collection_id.pk, 'carpeta': folder, 'número_de_imagen': image, 'texto_de_OCR': ocr_text, }
                            )

                            #move jpg files to static
                            #https://www.digitalocean.com/community/tutorials/how-to-set-up-object-storage-with-django
                            #https://boto3.readthedocs.io/en/latest/guide/migrations3.html#storing-data
                            #s3.Object('archivo', file).put(Body=open(path, 'rb'))
                            copyfile(path, '/srv/GAM/gam_app/static/documents/%s' % file)

                            #move thumbnail to static folder
                            parts = file.split('-')[:-1]
                            uuid = ''
                            for i in parts:
                                uuid += i + '-'
                            print(uuid[:-1])
                            thumbnail = '/tmp/DIP/' + dip_name + '/thumbnails/' + uuid[:-1] + '.jpg'

                            copyfile(thumbnail,'/srv/GAM/gam_app/static/thumbnails/%s' % file)

                            #create dzis for Openseadragon and move to static
                            try:
                                print('path is: %s' % path)
                                print('file is: %s' % file)
                                dzi_me = pyvips.Image.new_from_file(path)
                                dzi_me.dzsave('/srv/GAM/gam_app/dzis/%s' % file) 
                                subprocess.call('mv /srv/GAM/gam_app/dzis/%s.dzi /srv/GAM/gam_app/dzis/%s.dzi' % (file.split('.')[0], file))
                                subprocess.call('mv /srv/GAM/gam_app/dzis/%s_files /srv/GAM/gam_app/dzis/%s_files' %  (file.split('.')[0], file))
                            except:
                                print("Noo! exception!")
                                pass

                            #If letter at end of filename

                            '''
                               image= gam_des_001_001_004_001a  item = gam_des_001_001_004_001
                                      gam_des_001_001_004_002a         "
                                      gam_des_001_001_004_003          gam_des_001_001_004_003
                                      gam_des_001_001_004_004b         gam_des_001_001_004_004
                                      gam_des_001_001_004_005b         "
                                      gam_des_001_001_004_006b         "
                            '''

                            if re.search('[a-zA-Z]', image):
                                #Separate the numbers and letters in the filename
                                numbers = ''.join([i for i in image if i.isdigit()])
                                letters = ''.join([i for i in image if not i.isdigit()])
                                
                                # Find the first entry for that letter in the same folder
                                #print('Create list of images in the folder')
                                folder_images = Imagen.objects.filter(archivo__id=archivo_id.pk, colección__id=collection_id.pk, caja=str(box), legajo=str(bundle), carpeta=str(folder)).order_by('número_de_imagen')
                                #print('folder_images= ',folder_images)
                                for image in folder_images:
                                    image_letters = ''.join([i for i in image.número_de_imagen if not i.isdigit()])
                                    image_numbers = ''.join([i for i in image.número_de_imagen if i.isdigit()])  
                                    
                                    image_id = Imagen.objects.get(localizacion_fisica= physical_location)
                                    #print(image_id)
                                    # Folder images are sorted, so the first result with the same letter will be the item number.
                                    if letters == image_letters:
                                        
                                        Item.objects.update_or_create(
                                        nombre_del_item = archive+'_'+collection+'_'+box+'_'+bundle+'_'+folder+'_'+image_numbers,
                                        )

                                        my_item = Item.objects.get(nombre_del_item = archive+'_'+collection+'_'+box+'_'+bundle+'_'+folder+'_'+image_numbers)
                                        my_item.imágenes.add(image_id)
                                        # either of these should work, not sure which is better                                       
                                        #defaults= {'imágenes': image_id}
                                        #obj = Item.objects.get(nombre_del_item = archive+'_'+collection+'_'+box+'_'+bundle+'_'+folder+'_'+item_number,)
                                        #for key, value in defaults.items():
                                        #    setattr(obj, key, value)
                                        #    obj.save()
                                    
                                    else:
                                        Item.objects.update_or_create(
                                        nombre_del_item = archive+'_'+collection+'_'+box+'_'+bundle+'_'+folder+'_'+numbers,
                                        )

                                        my_item = Item.objects.get(nombre_del_item = archive+'_'+collection+'_'+box+'_'+bundle+'_'+folder+'_'+numbers)
                                        my_item.imágenes.add(image_id)
                                        #if this is the first time that the letter occurs in the folder
                                        
                            # Otherwise create a single-image item
                            else:
                                try:
                                    image_id = Imagen.objects.get(nombre_del_archivo= file)
                                except:
                                    image_id = Imagen.objects.filter(nombre_del_archivo= file)
                                    for image in image_id[1:]:
                                        image.delete()

                                Item.objects.update_or_create(
                                nombre_del_item = physical_location,
                                )
                                my_item = Item.objects.get(nombre_del_item = physical_location)
                                my_item.imágenes.add(image_id)
                #what to do with METs file
                #what is processing MCP file? 
                clean_dzis()


