from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
class lista(ListView):
    template_name = 'mi_aplication/lista.html'
    queryset = [
        'Gaudencio Lucas Bravo - Secretaría Académica, de Investigación e Innovación',
        'Rafael Portillo Rosales - Dirección de Docencia e Innovación Educativa',
        'Alfredo Hernández Ibarra - Coordinador de Capacitación Evaluación y certificación docente del TecNM',
        'Jorge Cein Villanueva Guzmán - Instructor del Curso'
        ]
    context_object_name = 'lista'
