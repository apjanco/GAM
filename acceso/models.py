from django.db import models
from gam_app.models import Persona, Imagen, Carpeta
from django.template.defaultfilters import slugify 
from ckeditor.fields import RichTextField

# Create your models here.
class Foto(models.Model):
    caso = models.ForeignKey('Caso', on_delete=models.CASCADE, default=1)
    file = models.FileField(upload_to='media/')

    def get_absolute_url(self):
        return "/media/%i/" % self.file

    def __str__(self):
        return str(self.file)

class Caso(models.Model):
    nombre_del_caso = models.CharField(max_length=200, blank=True)
    slug_name = models.SlugField(blank=True)
    carpetas = models.ManyToManyField(Carpeta, blank=True, related_name= 'caso_carpetas')
	#  Photos that will populate the slider section in index and caso
    fotos = models.ManyToManyField(Foto, blank=True, related_name= 'caso_fotos')
    descripción = RichTextField(blank=True, default='')

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.nombre_del_caso)
        super(Caso, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_del_caso