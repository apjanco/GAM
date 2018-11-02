import csv
import os
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *
from django.db.models import Count
import re


class Command(BaseCommand):
    """This is a command that will identify and remove duplicate records from the database.  After identifying 
    all records with count greater than two, the script checks if the texto_de_OCR field in one is empty.
    If one is not empty, it will favor the record with a transcription.  If neither have transcriptions, it will
    favor the older import over the newer."""
    help = "Check the database for duplicate records"
    def handle(self, *args, **options):
        #227 duplicate images at the moment
        #First, get a list of images that have a count greater than 1
        images = Imagen.objects.values('localizacion_fisica').annotate(count=Count('localizacion_fisica')).filter(count__gt=1)            
        print(len(images))
        for image in images: 
            name = image['localizacion_fisica']
            count = image['count']

            imagens = Imagen.objects.filter(localizacion_fisica=name)
            index = count - 1
            has_OCR = []
            bag_name = [] 

            while index >= 0:
                # print(imagens[index])
                if imagens[index].texto_de_OCR == '':
                    has_OCR.append("False")
                else:
                    has_OCR.append("True")
                
                #Getting only the numbers at the end of the bag name
                bag = re.search(r'\d+$', imagens[index].bag_name[-6:])
                if bag == None:
                    bag_name.append(0)
                else:
                    bag_name.append(int(bag.group()))
                index -= 1     

            print(has_OCR, bag_name)


            #These two lists are to check if both or neither have OCR text            
            true_list = ["True"] * len(has_OCR)
            false_list = ["False"] * len(has_OCR)

            # This is assuming there are only two duplicate images
            # Otherwise it should iterate through them
            if has_OCR == false_list:
                max_index = bag_name.index(max(bag_name))
                imagens[max_index].delete()
            elif has_OCR == true_list:
                print("Take a look at this one")
                pass
            else:
                index = has_OCR.index("False")
                imagens[index].delete()

