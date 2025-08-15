from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

# Create your views here.
def index(request):
    # Redirigir directamente al sistema de reuniones nacionales
    return redirect('index_reuniones')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def sistemas(request):
    return render(request, 'home/sistemas.html')

def desarrolloapps(request):
    return render(request, 'home/desarrolloapps.html')

def galeria(request):
    return render(request, 'home/galeria.html')



