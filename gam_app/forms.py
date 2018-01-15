# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.core.files.storage import FileSystemStorage
from gam_app.models import Imagen
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


		
class EditForm(forms.ModelForm):

	class Meta:
		model = Imagen
		fields = ['texto_de_OCR']

#https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
class crear_usuario(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )