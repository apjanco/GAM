from gam_app.models import *

def get_archivo_id(archivo):
	try:
		a_id = Archivo.objects.filter(nombre_del_archivo=archivo)
		for a in a_id:
			archivo_id = a.id
		return archivo_id
	except:
		archivo_id = 4
		return archivo_id

def get_colección_id(colección):
	try:
		c_id = Colección.objects.filter(nombre_de_la_colección=colección)
		for b in c_id:
			colección_id = b.id
		return colección_id
	except:
		colección_id = 1
		return colección_id