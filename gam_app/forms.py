# -*- coding: utf-8 -*-
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
import datetime

from django.db import models
from django.core.files.storage import FileSystemStorage
from gam_app.models import *
from mapwidgets.widgets import GooglePointFieldWidget, GoogleStaticMapWidget

class EditForm(forms.ModelForm):
    texto_de_OCR = forms.CharField(widget=CKEditorWidget(), required=False)
    #titulo_de_carpeta = forms.ModelMultipleChoiceField(queryset=Carpeta.objects.all())
    #This is the notes field for the folder
    notas = forms.CharField(widget=CKEditorWidget(), required=False)

    #STATUS_CHOICES = [('NONE','Sin correcciones'),('IN','En progreso'),('DONE','Compitió'),('FINAL','Competido y verificado')]
    #status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    class Meta:
        fields = ['texto_de_OCR', 'nombre_del_archivo','item','status','notas',]
        model = Imagen


class CarpetaForm(forms.ModelForm):
    class Meta:
        fields = ['carpeta_titulo', 'descripción']
        model = Carpeta
        widgets = { 'carpeta_titulo': forms.TextInput(attrs= {'size': 84 }),
                  }

class LugarAdminForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = '__all__'
        widgets = {
            'punto':GooglePointFieldWidget(settings={"GooglePointFieldWidget":(("zoom",8),)}),
        }

class LugarAdminStaticForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = '__all__'
        widgets = {
            'punto':GoogleStaticMapWidget,
        }

class SearchForm(forms.Form):
	search = forms.CharField(label='search', max_length=100)

clipboards = Portapapeles.objects.all()
CHOICES = []
count = 0
for item in clipboards:
	count += 1
	CHOICES.append((str(count),item.nombre_del_portapapeles))

class PortapapelesForm(forms.Form):
	list_name = forms.ChoiceField(choices=CHOICES)

def get_choice_list():
    return [Persona.nombre_de_la_persona for Persona in Persona.objects.all()]


class PersonaAutoForm(forms.ModelForm):
    nombre_de_la_persona = autocomplete.Select2ListCreateChoiceField(
        choice_list=get_choice_list,
        required=False,
        widget=autocomplete.ListSelect2(url='persona_name_lookup')
    )
    class Meta:
        fields = ['nombre_de_la_persona',]
        model = Persona

class PersonaForm(forms.ModelForm):
    class Meta:
        fields = ('__all__')
        model = Persona
        widgets = {
            'image': autocomplete.ModelSelect2Multiple(url='autocompletar_imagen')
        }

def get_choice_list_lugar():
    return [Lugar.nombre_del_lugar for Lugar in Lugar.objects.all()]


class LugarAutoForm(forms.ModelForm):
    nombre_del_lugar = autocomplete.Select2ListCreateChoiceField(
        choice_list=get_choice_list_lugar,
        required=False,
        widget=autocomplete.ListSelect2(url='lugar_name_lookup')
    )
    class Meta:
        fields = ['nombre_del_lugar',]
        model = Lugar

class LugarForm(forms.ModelForm):
    class Meta:
        fields = ('__all__')
        model = Lugar
        widgets = {
            'image': autocomplete.ModelSelect2Multiple(url='autocompletar_imagen')
        }

def get_choice_list_organizacion():
    return [Organización.nombre_de_la_organización for Organización in Organización.objects.all()]


class OrganizacionAutoForm(forms.ModelForm):
    nombre_de_la_organización = autocomplete.Select2ListCreateChoiceField(
        choice_list=get_choice_list_organizacion,
        required=False,
        widget=autocomplete.ListSelect2(url='organizacion_name_lookup')
    )
    class Meta:
        fields = ['nombre_de_la_organización',]
        model = Organización

class OrganizaciónForm(forms.ModelForm):
    class Meta:
        fields = ('__all__')
        model = Organización
        widgets = {
            'image': autocomplete.ModelSelect2Multiple(url='autocompletar_imagen')
        }

class CarpetaPersonaForm(forms.ModelForm):
    class Meta:
        fields = ['person_status',]
        model = Carpeta
