# -*- coding: utf-8 -*-
from django import forms
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


from django.db import models
from django.core.files.storage import FileSystemStorage
from gam_app.models import Imagen



		

class EditForm(forms.ModelForm):
    texto_de_OCR = forms.CharField(widget=CKEditorWidget())
    class Meta:
    	fields = ['texto_de_OCR', 'nombre_del_archivo']
    	model = Imagen

class SearchForm(forms.Form):
	search = forms.CharField(label='search', max_length=100)