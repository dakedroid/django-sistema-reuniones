from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Create your views here.
def index(request):
    return HttpResponse('<div style="font-family:sans-serif;background:#f8fafc;padding:40px 0;text-align:center;"><h1 style="color:#2563eb;margin-bottom:10px;">Hola Mundo</h1><small style="color:#64748b;font-size:18px;">Curso básico Django</small></div>')
