# -*- coding: utf-8 -*-
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from dal import autocomplete
import datetime

from django.db import models
from django.core.files.storage import FileSystemStorage
from gam_app.models import *


		

class EditForm(forms.ModelForm):
    texto_de_OCR = forms.CharField(widget=CKEditorWidget())
    #persona = forms.ModelChoiceField(queryset=Persona.objects.all(), required=False)

    #lugar = forms.ModelMultipleChoiceField(queryset=Lugar.objects.all())
    notas = forms.CharField(widget=CKEditorWidget(), required=False)
    fecha_desaparicion = forms.DateField(initial=datetime.date.today, required=False)
    CHOICES = [('HOMBRE','Hombre'), ('MUJER','Mujer'), ('OTRO','Otro')] 
    genero = forms.ChoiceField(choices=CHOICES, required=False)
   
    STATUS_CHOICES = [('NONE','Sin correcciones'),('IN','En progreso'),('DONE','Compitió'),('FINAL','Competido y verificado')]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    class Meta:
    	fields = ['texto_de_OCR', 'nombre_del_archivo', 'persona','ubicación_geográfica','actividades_políticas','fecha_desaparicion','genero','manuscritos','status','notas']
    	model = Imagen
    	widgets = {
		'persona': autocomplete.ModelSelect2Multiple(url='autocompletar', forward=['nombre_de_la_persona']),
    		'ubicación_geográfica': autocomplete.ModelSelect2Multiple(url='autocompletar_lugar', forward=['nombre_del_lugar']),
    		'actividades_políticas': autocomplete.ModelSelect2Multiple(url='autocompletar_organización', forward=['nombre_de_la_organización']),
            'manuscritos': autocomplete.ModelSelect2Multiple(url='autocompletar_manuscrito')
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

