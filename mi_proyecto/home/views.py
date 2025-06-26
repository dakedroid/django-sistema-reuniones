from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def sistemas(request):
    return render(request, 'home/sistemas.html')

def desarrolloapps(request):
    return render(request, 'home/desarrolloapps.html')



