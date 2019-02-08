from django.core.management.base import BaseCommand, CommandError
from gam_app.models import Imagen, Item

# 57 more images than items. Something seems wrong with this.


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Associating images with their host item.")

        all_imagens = Imagen.objects.all()

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
        for bag in bag_values:
            if (
                bag is not None
            ):  #  This is needed because some bag names are not true bags.  They reflect the name as we received it from Guatemala with spaces.
                if ' ' not in bag:
                    query_imagens = Imagen.objects.filter(bag_name=bag).order_by(
                        "número_de_imagen"
                    )
                    ### Is this query in order. Are the images in the order listed like in the example below???
                    # The order_by should handle this, but I am unser.

                    # Code adapted from import_dip.py
                    last_known_file_name = None
                    for image in query_imagens:
                        # Splitting the image filename. The image filename is similar to the item name.
                        # From taa1cf992-b86e-4eab-bcb2-5b45958hat, we can call the items by filename.
                        # If it fails, then its item name is the one above it that passed.
                        letters = ''.join(
                            [
                                i
                                for i in image.localizacion_fisica[8:]
                                if not i.isdigit()
                            ]
                        )
                        letters = letters[3:]
                        image_file = image.localizacion_fisica[: -len(letters)]
                        # The letters takes into account image files with endings with multiple letters.

                        # Retrieving the item from our information above
                        try:
                            my_item = Item.objects.get(nombre_del_item=image_file)
                            # If there is no item with that filename, it will raise an error.
                            image.item = my_item
                            last_known_file_name = my_item
                        except:
                            '''
                            image=  gam_des_001_001_004_001a  item = gam_des_001_001_004_001
                                    gam_des_001_001_004_002a         "
                                    gam_des_001_001_004_003          gam_des_001_001_004_003
                                    gam_des_001_001_004_004b         gam_des_001_001_004_004
                                    gam_des_001_001_004_005b         "
                                    gam_des_001_001_004_006b         "
                            '''
                            # Looking at this example, the second image would fail to find an item with its name
                            # It would instead look at the last known image that succeeded.
                            # It would then set its item information to that last known item, its 'host'.
                            image.item = last_known_file_name
                        image.save()
