from gam_app.models import *
def fun():
	images = Imagen.objects.all()
	for image in images:
		if len(image.caja) == 1:
			b = image(caja='00'+image.caja)
			b.save()