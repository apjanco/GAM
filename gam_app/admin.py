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
        model = FlatPage  # this is not automatically inherited from FlatpageFormOld


class FlatPageAdmin(FlatPageAdminOld):
    form = FlatpageForm


# We have to unregister the normal admin, and then reregister ours
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
# Register your models here.
class ImagenAdmin(admin.ModelAdmin):
    search_fields = ['localizacion_fisica', 'texto_de_OCR']
    list_display = [
        'localizacion_fisica',
        'colección',
        'caja',
        'legajo',
        'carpeta',
        'número_de_imagen',
        'status',
        'url',
    ]
    list_filter = ['status', 'bag_name']


admin.site.register(Imagen, ImagenAdmin)


class CarpetaAdmin(admin.ModelAdmin):
    search_fields = ['carpeta_titulo', 'caja', 'legajo', 'carpeta']
    list_filter = ['colección', 'caja', 'legajo', 'carpeta']


admin.site.register(Carpeta, CarpetaAdmin)


class PersonaAdmin(admin.ModelAdmin):
    search_fields = ['nombre_de_la_persona']


admin.site.register(Persona, PersonaAdmin)


class RelaciónAdmin(admin.ModelAdmin):
    search_fields = ['persona_A', 'persona_B']
    # autocomplete_fields = ['persona_A','persona_B',]


admin.site.register(Relación, RelaciónAdmin)


class LugarAdmin(admin.ModelAdmin):
    search_fields = ['lugar']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.form = LugarAdminForm
        else:
            # self.form = LugarAdminStaticForm
            self.form = LugarAdminForm
        return super(LugarAdmin, self).get_form(request, obj, **kwargs)


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


class CajaAdmin(admin.ModelAdmin):
    search_fields = ['número_de_caja']
    autocomplete_fields = ['carpetas']


admin.site.register(Caja, CajaAdmin)


class ItemAdmin(admin.ModelAdmin):
    search_fields = ['nombre_del_item']


admin.site.register(Item, ItemAdmin)


class TranscritoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transcrito, TranscritoAdmin)
