from django.db import models



# Create your models here.
class Person(models.Model):
    person_name = models.CharField(max_length=200, null=True)

class Place(models.Model):
    place_name = models.CharField(max_length=200, null=True)

class Organization(models.Model):
    organization_name = models.CharField(max_length=200, null=True)

class Document(models.Model):
    filename = models.CharField(max_length=200, blank=True)
    physical_location = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True, null=True)
    thumbnail = models.URLField(blank=True, null=True)
    #TODO enter physical location hierarchy
    archivo = models.CharField(max_length=200, blank=True)
    collection = models.CharField(max_length=200, blank=True)
    box = models.CharField(max_length=200, blank=True)
    bundle = models.CharField(max_length=200, blank=True)
    folder = models.CharField(max_length=200, blank=True)
    image = models.CharField(max_length=200, blank=True)

    ocr_text = models.TextField()
    def __str__(self):
   		return self.physical_location
    
                        
class Metadata(models.Model):
	physical_location = models.CharField(max_length=200, blank=True)
	case_name = models.ManyToManyField(Person, blank=True)
	date_of_disapearance = models.CharField(max_length=200, blank=True)
	page_count = models.IntegerField(blank=True)
	no_victims = models.IntegerField(blank=True)
	geographic_location = models.ManyToManyField(Place, blank=True)
	age_at_time = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=200, blank=True)
	ethnicity = models.CharField(max_length=200, blank=True)
	gam_form = models.CharField(max_length=200, blank=True)
	police_military = models.CharField(max_length=200, blank=True)
	kind_of_violence = models.CharField(max_length=200, blank=True)
	ngo_involvement = models.CharField(max_length=200, blank=True)
	political_activities = models.ManyToManyField(Organization, blank=True)
	profession = models.CharField(max_length=200, blank=True)
	notes = models.TextField()

class Database(models.Model):
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
	descripcion_caso = models.TextField()

















    

