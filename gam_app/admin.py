from django.contrib import admin
from gam_app.models import *

# Register your models here.
class DocumentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin) 


class PersonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Person, PersonAdmin) 

class PlaceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Place, PlaceAdmin) 

class OrganizationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Organization, OrganizationAdmin) 
