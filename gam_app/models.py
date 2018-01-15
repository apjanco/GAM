from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import DateTimeField



# Create your models here.
class Persona(models.Model):
    nombre_de_la_persona = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200, null=True)
    apellido_paterno = models.CharField(max_length=200, null=True)
    apellido_materno = models.CharField(max_length=200, null=True)
    def __str__(self):
   		return self.nombre_de_la_persona


class Lugar(models.Model):
    nombre_del_lugar = models.CharField(max_length=200, null=True)
    def __str__(self):
   		return self.nombre_del_lugar
    

class Organización(models.Model):
	nombre_de_la_organización = models.CharField(max_length=200, null=True)
	def __unicode__(self):
		return self.nombre_de_la_organización


    
              
class Caso(models.Model):
	caso = models.CharField(max_length=200, blank=True)
	fecha_desaparicion = models.CharField(max_length=200, blank=True)
	departamento = models.CharField(max_length=200, blank=True)
	local = models.CharField(max_length=200, blank=True)
	area = models.CharField(max_length=200, blank=True)
	ambiente = models.CharField(max_length=200, blank=True)
	estanteria_no = models.CharField(max_length=200, blank=True)
	plato_no = models.CharField(max_length=200, blank=True)
	caja_no = models.IntegerField(null=True, blank=True)
	legajo_no = models.IntegerField(null=True, blank=True)
	carpeta_no = models.IntegerField(null=True, blank=True)
	descripcion_caso = RichTextField()
	def __str__(self):
   		return self.caso

class Portapapeles(models.Model):
	usuario = models.ManyToManyField(User, blank=True)
	casos = models.ManyToManyField(Caso, blank=True)
	imágenes = models.ManyToManyField('Imagen', blank=True)
	manuscrito = models.ManyToManyField('Manuscrito', blank=True)
	def __str__(self):
   		return self.id

class Colección(models.Model):
	nombre_de_la_colección = models.CharField(max_length=200, blank=True)
	def __str__(self):
   		return self.nombre_de_la_colección

class Archivo(models.Model):
	nombre_del_archivo = models.CharField(max_length=200, blank=True)
	def __str__(self):
   		return self.nombre_del_archivo
   		
class Imagen(models.Model):
	persona = models.ManyToManyField('Persona', blank=True)
	nombre_del_archivo = models.CharField(max_length=200, blank=True)
	localizacion_fisica = models.CharField(max_length=200, blank=True)
	url = models.URLField(blank=True, null=True)
	miniatura = models.URLField(blank=True, null=True)
	archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE)
	colección = models.ForeignKey(Colección, on_delete=models.CASCADE)
	caja = models.IntegerField(null=True, blank=True)
	legajo = models.IntegerField(null=True, blank=True)
	carpeta = models.IntegerField(null=True, blank=True)
	#note that image number is CharField given use of 001a and 001b.
	número_de_imagen = models.CharField(max_length=200, blank=True)
	manuscritos = models.ManyToManyField('Manuscrito', blank=True)
	fecha_desaparicion = models.CharField(max_length=200, blank=True)
	conteo_de_páginas = models.IntegerField(null=True, blank=True)
	número_de_víctimas = models.IntegerField(null=True, blank=True)
	ubicación_geográfica = models.ManyToManyField('Lugar', blank=True)
	edad_en_el_momento = models.CharField(max_length=200, blank=True)
	género = models.CharField(max_length=200, blank=True)
	etnicidad = models.CharField(max_length=200, blank=True)
	forma_de_GAM = models.CharField(max_length=200, blank=True)
	policial_o_militar = models.CharField(max_length=200, blank=True)
	tipo_de_violencia= models.CharField(max_length=200, blank=True)
	participación_de_ONG = models.CharField(max_length=200, blank=True)
	actividades_políticas = models.ManyToManyField(Organización, blank=True)
	profesión = models.CharField(max_length=200, blank=True)
	texto_de_OCR = RichTextField()
	def __str__(self):
		return self.localizacion_fisica

class Manuscrito(models.Model):
    nombre_del_manuscrito = models.CharField(max_length=200, null=True)
    imágenes = models.ManyToManyField('Imagen', blank=True)
    def __str__(self):
   		return self.nombre_del_manuscrito

class Transcrito(models.Model):
	nombre_del_archivo = models.CharField(max_length=200, blank=False)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)
	tiempo_modificado = DateTimeField()
	texto_transcrito = RichTextField() 
