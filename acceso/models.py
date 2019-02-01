from django.db import models
from gam_app.models import Persona, Imagen, Carpeta
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
import django_filters

# Create your models here.
class Filtros(models.Model):
    nombre_del_filtro = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.nombre_del_filtro)



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
    carpetas = models.ManyToManyField(Carpeta, blank=True, related_name='caso_carpetas')
    #  profile image field doesn't work yet
    foto_de_perfil = models.OneToOneField(
        Foto,
        blank=True,
        related_name='caso_foto_de_perfil',
        on_delete=models.CASCADE,
        null=True,
    )
    #  Photos that will populate the slider section in index and caso

    fotos = models.ManyToManyField(Foto, blank=True, related_name='caso_fotos')
    descripción = RichTextField(blank=True, default='')
    filtros = models.ManyToManyField(Filtros, blank=True, related_name='caso_filtros')
    fecha_de_desaparicion = models.DateField(null=True, blank=True)

    def filters_list(self):
        filters_list = []
        for filter in self.filtros.values():
            filters_list.append(filter['nombre_del_filtro'])

        return str(filters_list).replace("'",'"')

    def save(self, *args, **kwargs):
        self.slug_name = slugify(self.nombre_del_caso)
        super(Caso, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre_del_caso

class CasoFilter(django_filters.FilterSet):
	nombre_del_caso = django_filters.CharFilter(lookup_expr='icontains')
	descripcion = django_filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Caso
		fields = ['nombre_del_caso', 'descripción']
