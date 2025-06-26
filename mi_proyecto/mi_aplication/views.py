from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import ListView
from .models import Estudiante, Carrera
from .forms import EstudianteForm, CarreraForm

# Create your views here.
class lista(ListView):
    template_name = 'mi_aplication/lista.html'
    queryset = ['Gaudencio Lucas Bravo - Secretaría Académica, de Investigación e Innovación',
                'Rafael Portillo Rosales - Dirección de Docencia e Innovación Educativa',
                  'Alfredo Hernández Ibarra - Coordinador de Capacitación Evaluación y certificación docente del TecNM',
                  'Jorge Cein Villanueva Guzmán - Instructor del Curso'] # type: ignore
    context_object_name = 'lista'

def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'mi_aplication/lista_estudiantes.html', {'estudiantes': estudiantes})

def detalle_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    return render(request, 'mi_aplication/detalle_estudiante.html', {'estudiante': estudiante})

def crear_estudiante(request):
    if request.method == "POST":
        estudiante_form = EstudianteForm(request.POST, request.FILES)
        if estudiante_form.is_valid():
            #Guarda el estudiante
            estudiante_form.save()
            return redirect('lista_estudiantes')
    else:
        estudiante_form = EstudianteForm()
    return render(request, 'mi_aplication/crear_estudiante.html',{
        'estudiante_form': estudiante_form
    })

def editar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        form = EstudianteForm(request.POST, request.FILES, instance=estudiante)
        if form.is_valid():
            form.save()
            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm(instance=estudiante)
    return render(request, 'mi_aplication/editar_estudiante.html', {'form':form})

def eliminar_estudiante(request, pk):
    estudiante = get_object_or_404(Estudiante, pk=pk)
    if request.method == "POST":
        estudiante.delete()
        return redirect('lista_estudiantes') # Redirige a la lista de estudiantes despues de eliminar
    return render(request, 'mi_aplication/eliminar_estudiante.html', {'estudiante':estudiante})

def crear_carrera(request):
    if request.method == "POST":
        form = CarreraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_carreras') # Cambiar el destino que prefieras despues de guardar
    else:
        form = CarreraForm()
    return render(request, 'mi_aplication/crear_carrera.html', {'form':form})

def lista_carreras(request):
    carreras = Carrera.objects.all()
    return render(request, 'mi_aplication/lista_carreras.html', {'carreras': carreras})