#!/usr/bin/env python
"""
Script para actualizar la base de datos con los nuevos campos del modelo Participante
"""

import os
import sys
import django

# Configurar Django
sys.path.append('/Users/molina/PycharmProjects/django-sistema-reuniones/mi_proyecto')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import Participante

def actualizar_base_datos():
    """Actualiza todos los participantes existentes con los nuevos campos"""
    
    print("🔄 Actualizando base de datos con nuevos campos...")
    
    try:
        # Obtener todos los participantes (Django ya maneja la conexión)
        participantes = Participante.objects.all()
        print(f"📊 Encontrados {len(participantes)} participantes para actualizar")
        
        contador_actualizados = 0
        
        for participante in participantes:
            actualizado = False
            
            # Agregar campos faltantes si no existen
            if not hasattr(participante, 'rfc') or participante.rfc is None:
                participante.rfc = ''
                actualizado = True
            
            if not hasattr(participante, 'curp') or participante.curp is None:
                participante.curp = ''
                actualizado = True
                
            if not hasattr(participante, 'sexo') or participante.sexo is None:
                participante.sexo = ''
                actualizado = True
                
            if not hasattr(participante, 'edad') or participante.edad is None:
                participante.edad = None
                actualizado = True
                
            if not hasattr(participante, 'director') or participante.director is None:
                participante.director = ''
                actualizado = True
                
            if not hasattr(participante, 'correo_direccion') or participante.correo_direccion is None:
                participante.correo_direccion = ''
                actualizado = True
                
            if not hasattr(participante, 'jefe_departamento') or participante.jefe_departamento is None:
                participante.jefe_departamento = ''
                actualizado = True
                
            if not hasattr(participante, 'correo_jefe_departamento') or participante.correo_jefe_departamento is None:
                participante.correo_jefe_departamento = ''
                actualizado = True
                
            if not hasattr(participante, 'area') or participante.area is None:
                participante.area = ''
                actualizado = True
                
            if not hasattr(participante, 'categoria_formativa') or participante.categoria_formativa is None:
                participante.categoria_formativa = ''
                actualizado = True
                
            if not hasattr(participante, 'cursos_especificos') or participante.cursos_especificos is None:
                participante.cursos_especificos = []
                actualizado = True
            
            # Guardar si se hicieron cambios
            if actualizado:
                try:
                    participante.save()
                    contador_actualizados += 1
                    print(f"✅ Actualizado: {participante.nombre} {participante.apellido_paterno}")
                except Exception as e:
                    print(f"❌ Error actualizando {participante.nombre}: {e}")
        
        print(f"\n🎉 ¡Actualización completada!")
        print(f"📊 Total de participantes actualizados: {contador_actualizados}")
        print(f"📊 Total de participantes: {len(participantes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la actualización: {e}")
        return False

def crear_participantes_prueba():
    """Crea algunos participantes de prueba con datos completos"""
    
    print("\n🧪 Creando participantes de prueba...")
    
    participantes_prueba = [
        {
            'nombre': 'Juan Carlos',
            'apellido_paterno': 'García',
            'apellido_materno': 'López',
            'rfc': 'GALJ800101ABC',
            'curp': 'GALJ800101HDFRPR01',
            'sexo': 'M',
            'edad': 43,
            'email': 'juan.garcia@tecnm.mx',
            'telefono': '555-1234567',
            'instituto': 'ITT_TIJUANA',
            'departamento': 'Sistemas Computacionales',
            'area': 'SISTEMAS_COMPUTACIONALES',
            'tipo_participante': 'DOCENTE',
            'director': 'Dr. María Elena Rodríguez',
            'correo_direccion': 'direccion@itt.mx',
            'jefe_departamento': 'Ing. Roberto Martínez',
            'correo_jefe_departamento': 'roberto.martinez@itt.mx',
            'categoria_formativa': 'DOCENTE',
            'cursos_especificos': ['CIENCIA_DATOS', 'INTELIGENCIA_ARTIFICIAL'],
            'confirmado': True
        },
        {
            'nombre': 'Ana Patricia',
            'apellido_paterno': 'Hernández',
            'apellido_materno': 'Silva',
            'rfc': 'HESA850315XYZ',
            'curp': 'HESA850315MDFRLN02',
            'sexo': 'F',
            'edad': 38,
            'email': 'ana.hernandez@tecnm.mx',
            'telefono': '555-7654321',
            'instituto': 'ITT_GUADALAJARA',
            'departamento': 'Administración',
            'area': 'ADMINISTRACION',
            'tipo_participante': 'ADMINISTRATIVO',
            'director': 'Dr. Carlos Mendoza',
            'correo_direccion': 'direccion@itg.mx',
            'jefe_departamento': 'Lic. Sandra Torres',
            'correo_jefe_departamento': 'sandra.torres@itg.mx',
            'categoria_formativa': 'ADMINISTRATIVO',
            'cursos_especificos': ['LIDERAZGO', 'GESTION_PROYECTOS'],
            'confirmado': True
        },
        {
            'nombre': 'Luis Fernando',
            'apellido_paterno': 'Morales',
            'apellido_materno': 'Castro',
            'rfc': 'MOCL750620DEF',
            'curp': 'MOCL750620HDFRTS03',
            'sexo': 'M',
            'edad': 48,
            'email': 'luis.morales@tecnm.mx',
            'telefono': '555-9876543',
            'instituto': 'ITT_MONTERREY',
            'departamento': 'Dirección',
            'area': 'DIRECCION',
            'tipo_participante': 'DIRECTOR',
            'director': 'El mismo (Director)',
            'correo_direccion': 'luis.morales@tecnm.mx',
            'jefe_departamento': 'N/A',
            'correo_jefe_departamento': '',
            'categoria_formativa': 'DIRECTIVO',
            'cursos_especificos': ['PLANEACION_ESTRATEGICA', 'CALIDAD_EDUCATIVA'],
            'confirmado': True
        }
    ]
    
    try:
        for datos in participantes_prueba:
            # Verificar si ya existe
            if Participante.objects.filter(email=datos['email']).first():
                print(f"⚠️  Ya existe: {datos['nombre']} {datos['apellido_paterno']}")
                continue
                
            participante = Participante(**datos)
            participante.save()
            print(f"✅ Creado: {participante.nombre} {participante.apellido_paterno}")
            
        print("\n🎉 ¡Participantes de prueba creados!")
        
    except Exception as e:
        print(f"❌ Error creando participantes de prueba: {e}")

if __name__ == "__main__":
    print("🛠️  Actualización de Base de Datos - TecNM")
    print("=" * 50)
    
    # Actualizar participantes existentes
    if actualizar_base_datos():
        # Crear participantes de prueba
        crear_participantes_prueba()
        print("\n✅ ¡Proceso completado! Ya puedes usar la aplicación.")
    else:
        print("\n❌ Hubo errores en la actualización.")