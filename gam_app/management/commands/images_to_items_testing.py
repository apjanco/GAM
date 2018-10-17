from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen, Item
import re
# 57 more images than items. Something seems wrong with this.

class CurrentItem:
    """An object to hold the value of the current bag and letters"""
    def __init__(self, name, letters):
         self.name = name
         self.letters = letters

class Command(BaseCommand):


    def handle(self, *args, **options):
        print("Associating images with their host item.")

        all_imagens = Imagen.objects.all()
        current_item = CurrentItem

        #Getting all bag values
        bag_values = []
        for image in all_imagens:
            if image.bag_name not in bag_values:
                bag_values.append(image.bag_name)

        # Now iterate over bag values and make a query
        # With each query, run some code that reads the filename
        # and updates the image item field with the item
        # it is associated with

        # Variable to keep track of filenames
        bags = {}
        for bag in bag_values:
            if bag is not None:  #  This is needed because some bag names are not true bags.  They reflect the name as we received it from Guatemala with spaces.
                if ' ' not in bag:
                    bags[bag] = {}
                    query_imagens = Imagen.objects.filter(bag_name= bag).order_by("caja","legajo","carpeta","número_de_imagen")

                    #  create a list from the queryset that will allow indexing
                    imagens_list = []
                    for item in query_imagens:
                        imagens_list.append(item.nombre_del_archivo)
                    #print(imagens_list)

                    for index, image in enumerate(imagens_list):
                        número_de_imagen = image.split('.')[0]
                        número_de_imagen = número_de_imagen.split('_')[-1]

                        # file number has letter
                        if re.search('[a-zA-Z]', número_de_imagen):
                            letters = ''.join([i for i in número_de_imagen if not i.isdigit()])

                            #  check previous image, if previous had no letters
                            if not letters in imagens_list[index-1].split('.')[0].split('_')[-1]:

                                #  create an item from physical location minus letters
                                item_name = image.split('.')[0].split('-')[-1][:-len(letters)]
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
                                    print('[*] Error with {}'.format(current_item.name))
                                    continue

# file number has no letters :: create single-image item
                        else:
                            #print('single-image item: ',image.localizacion_fisica)
                            bags[bag][image.split('.')[0].split('-')[-1]] = []
                            bags[bag][image.split('.')[0].split('-')[-1]].append(image)


        #Item.objects.all().delete()

        for key, value in bags.items():
            for value1 in value.items():
                # get item with name in the list
                try:
                    item = Item.objects.get(nombre_del_item= value1[0])
                except:
                    item = Item(nombre_del_item= value1[0])
                    item.save()

                for file in value1[1]:
                     image = Imagen.objects.get(nombre_del_archivo= file)
                     image.item = item
                     image.save()
        #print(bags['agos29_2018_bag106'])
        #print(bags['nov9_2017_bag3'])
        #print(bags['Agos24_2018_bag101'])
        #print(bags['Dic06_17_bag8'])
