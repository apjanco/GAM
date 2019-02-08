### Please review this script.  Thank you!! ###

from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen, Item
import re


class CurrentItem:
    """An object to hold the current bag and letters values. Values are written
    by the first image with a particular letter pattern (a, bbb, cc).  As the script moves 
    down the list, later occurances of that pattern are written to the initial item.  
    This prevents the creation of multiple items for a given letter pattern."""

    def __init__(self, name, letters):
        self.name = name
        self.letters = letters


class Command(BaseCommand):
    """This is a script for generating the relationships between images and items in the collection.  An image is a single scan of a document. An item can 
    contain one or more images.  It is typically used when we have scanned the front and back of a document or there are several pages in the same form.
    An item associates the images that are part of the item in the database.

    During scanning in Guatemala, the staff indicate that images are part of a common item by adding a letter to the number of the filename.
    This typically happens sequentially, but often the letters start and restart based on folders, boxes or other reasons that are not clear.
    Nonetheless, images in an item are nearly always next to eachother.  So 001a and 002a should, in most cases, be part of the same item.
    However, 001a, 002a...008a and 020a are likely three separate items.

    To address this problem, this script sorts all of the image files so that associated images will be proximate to one another.

    The script moves down the list of sorted images.  Where no letter is present, a single-image item is created.

    Where there is a letter in the file number, the script checks the previous entry for a letter.  If none is present, then a new item is created.
    For the next row, we check if a letter is present.  If the letter matches that of the most recently created item (presumably the row before),
    then the image is added to the current item.  If the letter is not the same, then a new item is created.  
        """

    def handle(self, *args, **options):
        print("Associating images with their host item.")

        all_imagens = Imagen.objects.all()
        current_item = CurrentItem

        # Getting all bag values
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
            if ' ' not in bag:
                bags[bag] = {}
                query_imagens = Imagen.objects.filter(bag_name=bag).order_by(
                    "caja", "legajo", "carpeta", "número_de_imagen"
                )

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
                            [i for i in número_de_imagen if not i.isdigit()]
                        )

                        #  check previous image, if previous had no letters
                        if (
                            letters
                            not in imagens_list[index - 1].split('.')[0].split('_')[-1]
                        ):

                            #  create an item from physical
                            #  location minus letters
                            item_name = image.split('.')[0].split('-')[-1][
                                : -len(letters)
                            ]
                            bags[bag][item_name] = []

                            #  add current image to the item
                            bags[bag][item_name].append(image)

                            #  variable to hold current item name
                            current_item.name = item_name
                            current_item.letters = letters

                        #  Check if letters are the same. if current item letters matches image letters, add to current item
                        elif (
                            letters
                            and current_item.letters
                            in imagens_list[index - 1].split('.')[0].split('_')[-1]
                        ):
                            try:
                                bags[bag][current_item.name].append(image)

                            except:
                                print('[*] Error with {}'.format(current_item.name))
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
