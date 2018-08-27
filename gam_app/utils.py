from gam_app.models import *
import googleapiclient.discovery

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

#A function using the Google Natural Language API to identify entites (such as PERSON) in text.
# may require $ export GOOGLE_APPLICATION_CREDENTIALS='/home/ajanco/DS-GAM-7fa5231f373f.json'
#source: https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/language/api/analyze.py
def get_entities(text, encoding='UTF32'):
	body = { 'document': {'type': 'PLAIN_TEXT','content': text,}, 'encoding_type': encoding,}
	
	service = googleapiclient.discovery.build('language', 'v1')
	
	request = service.documents().analyzeEntities(body=body)
	
	response = request.execute()
	#type = response['entities'][0]['type']

	return response


