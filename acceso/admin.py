from django.contrib import admin
from acceso.models import *

# Register your models here.
class CasoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Caso, CasoAdmin)

class FotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Foto, FotoAdmin)