# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.core.files.storage import FileSystemStorage
from gam_app.models import Imagen
		
class EditForm(forms.ModelForm):

	class Meta:
		model = Imagen
		fields = ['texto_de_OCR']