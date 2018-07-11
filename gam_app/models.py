from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db.models import DateTimeField
from django.urls import reverse
from django.contrib.sites.models import Site

#This is a person.
class Persona(models.Model):
    nombre_de_la_persona = models.CharField(max_length=200, null=True)
    nombre = models.CharField(max_length=200, null=True)
    segundos_nombre = models.CharField(max_length=200, null=True)
    apellido_paterno = models.CharField(max_length=200, null=True)
    apellido_materno = models.CharField(max_length=200, null=True)
    fecha_de_nacimiento = models.CharField(max_length=200, null=True)
    fecha_desaparicion = models.CharField(max_length=200, blank=True)
    edad_en_el_momento = models.CharField(max_length=200, blank=True)
    género = models.CharField(max_length=200, blank=True)
    etnicidad = models.CharField(max_length=200, blank=True)
    profesión = models.CharField(max_length=200, blank=True)
    actividades_políticas = models.ManyToManyField('Organización', blank=True)
    #relaciones = models.ManyToManyField('Relación', blank=True)
    notas = RichTextField(blank=True)

    def __str__(self):
       return self.nombre_de_la_persona

#relationships 
#class Relación(models.Model):
    #personA = models.ManyToManyField(Persona, blank=True)
    #personB = models.ManyToManyField(Persona, blank=True)
 #   relationship = models.CharField(max_length=200, choices=(('s', 'esposa'),
  #                                           ('c', 'niño'),
   #                                          ('p', 'padre')),
    #                                          default='s')

#This is a place.
class Lugar(models.Model):
    nombre_del_lugar = models.CharField(max_length=200, null=True)

    def __str__(self):
       return self.nombre_del_lugar

# An organization entity.  Typically refers to a political organziation that a person was affiliated with.
class Organización(models.Model):
    nombre_de_la_organización = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.nombre_de_la_organización



#This one is complicated.  Basically, these are bundles of papers that were put together as the workers at GAM investigated
#a report or request for information.  They were later put into folders together under a "case" title.  The title often refers to
#one or more people involved in the case (so they look like names), but they refer to a "case."  This list of cases is being
#used by the archive team in Guatemala to process and catalog the materials.  It's not clear how this will work out in the
#long term.
class Caso(models.Model):
    caso = models.CharField(max_length=200, blank=True)
    fecha_desaparicion = models.CharField(max_length=200, blank=True)
    departamento = models.CharField(max_length=200, blank=True)
    local = models.CharField(max_length=200, blank=True)
    area = models.CharField(max_length=200, blank=True)
    ambiente = models.CharField(max_length=200, blank=True)
    estanteria_no = models.CharField(max_length=200, blank=True)
    plato_no = models.CharField(max_length=200, blank=True)
    caja_no = models.CharField(max_length=200, blank=True)
    legajo_no = models.CharField(max_length=200, blank=True)
    carpeta_no = models.CharField(max_length=200, blank=True)
    descripcion_caso = RichTextField()

    def __str__(self):
       return self.caso

#Clipboard.  An entity for creating lists of individual images, manuscripts and cases for users during research.
#For example, a member of the legal team may want to include all the documents they have come across that relate to
#a current case.
class Portapapeles(models.Model):
    nombre_del_portapapeles = models.CharField(max_length=200, blank=True)
    usuario = models.ManyToManyField(User, blank=True)
    casos = models.ManyToManyField(Caso, blank=True)
    imágenes = models.ManyToManyField('Imagen', blank=True)
    manuscrito = models.ManyToManyField('Item', blank=True)

    def __str__(self):
       return self.nombre_del_portapapeles

#Folder
class Carpeta(models.Model):
    carpeta_titulo = models.CharField(max_length=200, blank=True)
    personas = models.ManyToManyField('Persona', blank=True)
    nombre_de_la_carpeta = models.CharField(max_length=200, blank=True)
    archivo = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    colección = models.ForeignKey('Colección', on_delete=models.CASCADE)
    caja = models.CharField(max_length=200, blank=True)
    legajo = models.CharField(max_length=200, blank=True)
    carpeta = models.CharField(max_length=200, blank=True)
    número_de_víctimas = models.IntegerField(null=True, blank=True)
    ubicación_geográfica = models.ManyToManyField('Lugar', blank=True)
    tipo_de_violencia= models.CharField(max_length=200, blank=True)
    descripción = RichTextField(blank=True, default='')
    descripción_generada_automaticamente = RichTextField(blank=True)

    def __str__(self):
       return '%s/%s/%s' % (self.caja,self.legajo,self.carpeta)

#This is an archival collection
class Colección(models.Model):
    archivo = models.ForeignKey('Archivo', on_delete=models.CASCADE)
    nombre_de_la_colección = models.CharField(max_length=200, blank=True)
    descripción = RichTextField(blank=True, default='')

    def __str__(self):
       return self.nombre_de_la_colección

# Archivo means both archive and file in Spanish.  This model refers to an Archive, as in The Archives of GAM or
# The Internet Archive
class Archivo(models.Model):
    nombre_del_archivo = models.CharField(max_length=200, blank=True)
    descripción = RichTextField(blank=True, default='')
    def __str__(self):
       return self.nombre_del_archivo

STATUS_CHOICES = (
        ('NONE','Sin correcciones'),
        ('IN','En progreso'),
        ('DONE','Compitió'),
        ('FINAL','Competido y verificado')
)
# This is the model for an image in the archive.  It's the core entity in the data model.
class Imagen(models.Model):
    #persona = models.ManyToManyField('Persona', blank=True)
    nombre_del_archivo = models.CharField(max_length=200, blank=True)
    localizacion_fisica = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True, null=True)
    miniatura = models.URLField(blank=True, null=True)
    archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE, default=1)
    colección = models.ForeignKey(Colección, on_delete=models.CASCADE, default=1)
    caja = models.CharField(max_length=200, blank=True)
    legajo = models.CharField(max_length=200, blank=True)
    carpeta = models.CharField(max_length=200, blank=True)
    #note that image number is CharField given use of 001a and 001b.
    número_de_imagen = models.CharField(max_length=200, blank=True)
    manuscritos = models.ManyToManyField('Item', blank=True)
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
    texto_de_OCR = RichTextField(blank=True)
    notas = RichTextField(blank=True)
    traducción = RichTextField(blank=True)
    status = models.CharField(max_length= 20, choices=STATUS_CHOICES)
    bag_name = models.CharField(max_length=200, blank=True) 

    def __str__(self):
        return self.localizacion_fisica

    def get_absolute_url(self):
        return reverse('documento5', args=[self.archivo, self.colección, self.caja, self.legajo,
                                           self.carpeta, self.número_de_imagen])

    def get_image_url(self):
        return '/static/documents/' + self.nombre_del_archivo

# This is an entity to link single-page images together as part of multi-page documents such as a pamphlet or book.
class Item(models.Model):
    nombre_del_item = models.CharField(max_length=200, null=True)
    imágenes = models.ManyToManyField('Imagen', blank=True)
    sites = models.ManyToManyField(Site)

    def __str__(self):
       return self.nombre_del_item

# Transcriptions, these work with the machine readable text associated with an image.  The text is initially ocr'd with Google Vision.
# When a user maker a correction, the previous version is saved here.
class Transcrito(models.Model):
    nombre_del_archivo = models.CharField(max_length=200, blank=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tiempo_modificado = DateTimeField()
    texto_transcrito = RichTextField()
