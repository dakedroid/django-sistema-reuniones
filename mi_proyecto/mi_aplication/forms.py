from django import forms 
from .models import Estudiante, Carrera

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'appat', 'apmat', 'matricula', 'curp', 'fotografia', 'carrera']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control'}),
            'appat': forms.TextInput(attrs={'placeholder': 'Apellido Paterno', 'class': 'form-control'}),
            'apmat': forms.TextInput(attrs={'placeholder': 'Apellido Materno', 'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'placeholder': 'Matrícula', 'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'placeholder': 'CURP', 'class': 'form-control'}),
            'fotografia': forms.ClearableFileInput(),
        }
        labels = {
            'nombre': 'Nombre',
            'appat': 'Apellido Paterno',
            'apmat': 'Apellido Materno',
            'matricula': 'Matrícula',
            'curp': 'CURP',
            'carrera': 'Carrera',
            'fotografia': 'Fotografía',
        }

class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = ['nombre', 'clave', 'modalidad']
        widgets = {
            'nombre' : forms.TextInput(attrs={'placeholder':'Nombre de la Carrera', 'class': 'form-control'}),
            'clave': forms.TextInput(attrs={'placeholder': 'Clave', 'class': 'form-control'}),
            'modalidad': forms.Select(attrs={'placeholder': 'Modalidad', 'class': 'form-select'})
        }
        labels = {
            'nombre': 'Nombre',
            'clave': 'Clave',
            'modalidad': 'Modalidad'
        }