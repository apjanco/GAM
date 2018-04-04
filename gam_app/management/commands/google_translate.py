#import sys
#import os
#from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from gam_app.models import *
import googleapiclient.discovery
from google.cloud import translate
#import base64
#import io
#import pprint
#import shutil
#import subprocess
#from PIL import Image
#import boto3
#s3 = boto3.resource('s3')
#from shutil import copyfile
#import pyvips
from gam_app.settings_secret import API_KEY

def get_translation(rich_text):
	translate_client = translate.Client()
	translation = translate_client.translate(rich_text,target_language='en',source_language='es')
	return translation['translatedText']

class Command(BaseCommand):
	help = "Imports translations from the google translate API into the database"
	def handle(self, *args, **options):
		i = 0
		for imagen in Imagen.objects.all():
			if i%10 == 0:
				print(i)
			if not imagen.traducción:
				texto = imagen.texto_de_OCR
				imagen.traducción = get_translation(texto)
				imagen.save()
			i += 1
