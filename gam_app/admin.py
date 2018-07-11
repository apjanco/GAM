from django.contrib import admin
from gam_app.models import *
from django.contrib.flatpages.models import FlatPage


# Note: we are renaming the original Admin and Form as we import them!
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld
from django.contrib.flatpages.admin import FlatpageForm as FlatpageFormOld

from django import forms
from ckeditor.widgets import CKEditorWidget
from gam_app.forms import *

class FlatpageForm(FlatpageFormOld):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
    	fields = '__all__'
    	model = FlatPage # this is not automatically inherited from FlatpageFormOld


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
# Register your models here.
class ImagenAdmin(admin.ModelAdmin):
    search_fields = [ 'localizacion_fisica', 'texto_de_OCR', ]
    list_display = ['colección', 'caja', 'legajo', 'carpeta', 'número_de_imagen']
    list_filter = ['status']
admin.site.register(Imagen, ImagenAdmin) 

class CarpetaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Carpeta, CarpetaAdmin)



class PersonaAdmin(admin.ModelAdmin):
    pass
admin.site.register(Persona, PersonaAdmin) 

class LugarAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lugar, LugarAdmin) 

class OrganizaciónAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organización, OrganizaciónAdmin)

class CasoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Caso, CasoAdmin) 

class PortapapelesAdmin(admin.ModelAdmin):
    pass

admin.site.register(Portapapeles, PortapapelesAdmin)

class ArchivoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Archivo, ArchivoAdmin)

class ColecciónAdmin(admin.ModelAdmin):
    pass

admin.site.register(Colección, ColecciónAdmin)

class ItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Item, ItemAdmin)

class TranscritoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Transcrito, TranscritoAdmin)
