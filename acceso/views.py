from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'acceso/index.html', {})

def about(request):
    return render(request, 'acceso/about.html', {})

def map(request):
    return render(request, 'acceso/map.html', {})


def history(request):
    return render(request, 'acceso/history.html', {})












