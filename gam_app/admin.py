from django.contrib import admin
from gam_app.models import *

# Register your models here.
class ImagenAdmin(admin.ModelAdmin):
    pass

admin.site.register(Imagen, ImagenAdmin) 


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
