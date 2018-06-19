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
    #titulo_de_carpeta = forms.ModelMultipleChoiceField(queryset=Carpeta.objects.all())
    #This is the notes field for the folder
    notas = forms.CharField(widget=CKEditorWidget(), required=False)

    STATUS_CHOICES = [('NONE','Sin correcciones'),('IN','En progreso'),('DONE','Compitió'),('FINAL','Competido y verificado')]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    class Meta:
        fields = ['texto_de_OCR', 'nombre_del_archivo','manuscritos','status','notas',]
        model = Imagen


class CarpetaForm(forms.ModelForm):
    class Meta:
        fields = ['carpeta_titulo', 'descripción']
        model = Carpeta
        widgets = { 'carpeta_titulo': forms.TextInput(attrs= {'size': 84 }),
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

