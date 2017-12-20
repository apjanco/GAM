from django.shortcuts import render
from .models import Document
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse



# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
	return render(request, 'index.html')

def document(request, filename):
	state = get_object_or_404(Document, filename=filename)
	context  = {'state':state}
	return render(request, 'document_page.html', context)
