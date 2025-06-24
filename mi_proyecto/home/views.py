from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Create your views here.
def index(request):
    return HttpResponse('<div style="font-family:sans-serif;padding:40px 0;text-align:center;">'
        '<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7J1KxKrEdI46kp0QbEHejSoGQMfXIZ_bWUg&s" alt="Imagen" style="width:120px;height:120px;display:block;margin:0 auto 20px;animation:latido 1s infinite;">'
        '<h1 style="color:#2563eb;margin-bottom:10px;">Hola Mundo</h1>'
        '<small style="color:#64748b;font-size:18px;">Curso básico Django</small>'
        '<style>@keyframes latido {0% {transform: scale(1);} 20% {transform: scale(1.1);} 40% {transform: scale(0.95);} 60% {transform: scale(1.05);} 80% {transform: scale(0.97);} 100% {transform: scale(1);}}</style>'
    '</div>')