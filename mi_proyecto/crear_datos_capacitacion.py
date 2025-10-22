#!/usr/bin/env python
"""
Script para crear datos de prueba del sistema de capacitaciones TecNM
Ejecutar: python manage.py shell < crear_datos_capacitacion.py
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import Participante, ReunionNacional, Acuerdo
from mi_aplication.constants import (
    TIPOS_PARTICIPANTE, CATEGORIAS_FORMATIVAS, CURSOS_ESPECIFICOS,
    PLANTELES_TECNM, AREAS_DEPARTAMENTO, SEXOS, TIPOS_REUNION,
    ESTADOS_REUNION, MODALIDADES_REUNION
)

def crear_participantes_ejemplo():
    """Crear participantes de ejemplo con datos de capacitación"""
    
    participantes_datos = [
        # Directivos
        {
            'nombre': 'María Elena',
            'apellido_paterno': 'González',
            'apellido_materno': 'Martínez',
            'rfc': 'GOMM850615H01',
            'curp': 'GOMM850615MDFNMR01',
            'sexo': 'F',
            'edad': 39,
            'email': 'direccion@ittijuana.edu.mx',
            'telefono': '+52 664 123 4567',
            'instituto': 'ITT_TIJUANA',
            'area': 'DIRECCION',
            'tipo_participante': 'DIRECTOR',
            'director': 'María Elena González Martínez',
            'correo_direccion': 'direccion@ittijuana.edu.mx',
            'categoria_formativa': 'DIRECTIVO',
            'cursos_especificos': ['LIDERAZGO', 'GESTION_PROYECTOS', 'PLANEACION_ESTRATEGICA']
        },
        {
            'nombre': 'Roberto',
            'apellido_paterno': 'Hernández',
            'apellido_materno': 'López',
            'rfc': 'HELR780923H02',
            'curp': 'HELR780923HDFPPR02',
            'sexo': 'M',
            'edad': 46,
            'email': 'roberto.hernandez@itmexico.edu.mx',
            'telefono': '+52 55 987 6543',
            'instituto': 'ITT_TOLUCA',
            'area': 'SUBDIRECCION_ACADEMICA',
            'tipo_participante': 'SUBDIRECTOR',
            'director': 'Ana Sofía Pérez Ramírez',
            'correo_direccion': 'direccion@itmexico.edu.mx',
            'jefe_departamento': 'Ana Sofía Pérez Ramírez',
            'correo_jefe_departamento': 'direccion@itmexico.edu.mx',
            'categoria_formativa': 'DIRECTIVO',
            'cursos_especificos': ['CALIDAD_EDUCATIVA', 'EVALUACION_EDUCATIVA', 'METODOLOGIA_INVESTIGACION']
        },
        
        # Docentes
        {
            'nombre': 'Carlos',
            'apellido_paterno': 'Ruiz',
            'apellido_materno': 'Fernández',
            'rfc': 'RUFC890415H03',
            'curp': 'RUFC890415HDFRNR03',
            'sexo': 'M',
            'edad': 35,
            'email': 'carlos.ruiz@itsistemas.edu.mx',
            'telefono': '+52 33 456 7890',
            'instituto': 'ITT_GUADALAJARA',
            'area': 'SISTEMAS_COMPUTACIONALES',
            'tipo_participante': 'DOCENTE',
            'director': 'Luis Alberto Méndez Torres',
            'correo_direccion': 'direccion@itgdl.edu.mx',
            'jefe_departamento': 'Patricia Silva Rodríguez',
            'correo_jefe_departamento': 'sistemas@itgdl.edu.mx',
            'categoria_formativa': 'DOCENTE',
            'cursos_especificos': ['CIENCIA_DATOS', 'INTELIGENCIA_ARTIFICIAL', 'MACHINE_LEARNING']
        },
        {
            'nombre': 'Ana Patricia',
            'apellido_paterno': 'Morales',
            'apellido_materno': 'García',
            'rfc': 'MOGA920607F04',
            'curp': 'MOGA920607MDFRCN04',
            'sexo': 'F',
            'edad': 32,
            'email': 'ana.morales@itnorte.edu.mx',
            'telefono': '+52 81 234 5678',
            'instituto': 'ITT_MONTERREY',
            'area': 'MATEMATICAS',
            'tipo_participante': 'DOCENTE',
            'director': 'Javier Ramírez Sánchez',
            'correo_direccion': 'direccion@itmty.edu.mx',
            'jefe_departamento': 'Eduardo Santos Villarreal',
            'correo_jefe_departamento': 'matematicas@itmty.edu.mx',
            'categoria_formativa': 'DOCENTE',
            'cursos_especificos': ['ESTADISTICA_AVANZADA', 'METODOLOGIA_INVESTIGACION', 'PEDAGOGIA_DIGITAL']
        },
        {
            'nombre': 'Fernando',
            'apellido_paterno': 'Jiménez',
            'apellido_materno': 'Vásquez',
            'rfc': 'JIVF871220H05',
            'curp': 'JIVF871220HDFMSF05',
            'sexo': 'M',
            'edad': 37,
            'email': 'fernando.jimenez@itsur.edu.mx',
            'telefono': '+52 967 345 6789',
            'instituto': 'ITT_TUXTLA_GUTIERREZ',
            'area': 'INDUSTRIAL',
            'tipo_participante': 'DOCENTE',
            'director': 'Claudia Esperanza Flores Ruiz',
            'correo_direccion': 'direccion@itsur.edu.mx',
            'jefe_departamento': 'Manuel Ordóñez Castro',
            'correo_jefe_departamento': 'industrial@itsur.edu.mx',
            'categoria_formativa': 'DOCENTE',
            'cursos_especificos': ['GESTION_PROYECTOS', 'SUSTENTABILIDAD', 'INNOVACION_EDUCATIVA']
        },
        
        # Personal Administrativo
        {
            'nombre': 'Lucía',
            'apellido_paterno': 'Torres',
            'apellido_materno': 'Mendoza',
            'rfc': 'TOML830518F06',
            'curp': 'TOML830518MDFRNC06',
            'sexo': 'F',
            'edad': 41,
            'email': 'lucia.torres@itoeste.edu.mx',
            'telefono': '+52 664 567 8901',
            'instituto': 'ITT_TIJUANA',
            'area': 'RECURSOS_HUMANOS',
            'tipo_participante': 'ADMINISTRATIVO',
            'director': 'María Elena González Martínez',
            'correo_direccion': 'direccion@ittijuana.edu.mx',
            'jefe_departamento': 'Sandra Milena Ruiz Torres',
            'correo_jefe_departamento': 'rh@ittijuana.edu.mx',
            'categoria_formativa': 'ADMINISTRATIVO',
            'cursos_especificos': ['RECURSOS_HUMANOS', 'ADMINISTRACION_PUBLICA', 'LIDERAZGO']
        },
        
        # Investigadores
        {
            'nombre': 'Dr. Miguel',
            'apellido_paterno': 'Rodríguez',
            'apellido_materno': 'Pérez',
            'rfc': 'ROPM750310H07',
            'curp': 'ROPM750310HDFDRG07',
            'sexo': 'M',
            'edad': 49,
            'email': 'miguel.rodriguez@itcentro.edu.mx',
            'telefono': '+52 442 678 9012',
            'instituto': 'ITT_QUERETARO',
            'area': 'INVESTIGACION',
            'tipo_participante': 'INVESTIGADOR',
            'director': 'Dra. Carmen Leticia Borrayo Rodríguez',
            'correo_direccion': 'direccion@itqro.edu.mx',
            'jefe_departamento': 'Dr. Alejandro Medina Carrera',
            'correo_jefe_departamento': 'investigacion@itqro.edu.mx',
            'categoria_formativa': 'INVESTIGADOR',
            'cursos_especificos': ['METODOLOGIA_INVESTIGACION', 'BIG_DATA', 'CIBERSEGURIDAD', 'BLOCKCHAIN']
        },
    ]
    
    print("Creando participantes de ejemplo...")
    participantes_creados = []
    
    for datos in participantes_datos:
        try:
            # Verificar si ya existe
            if Participante.objects.filter(email=datos['email']).first():
                print(f"  - Participante con email {datos['email']} ya existe, saltando...")
                continue
                
            participante = Participante(
                nombre=datos['nombre'],
                apellido_paterno=datos['apellido_paterno'],
                apellido_materno=datos['apellido_materno'],
                rfc=datos['rfc'],
                curp=datos['curp'],
                sexo=datos['sexo'],
                edad=datos['edad'],
                email=datos['email'],
                telefono=datos['telefono'],
                instituto=datos['instituto'],
                area=datos['area'],
                tipo_participante=datos['tipo_participante'],
                director=datos['director'],
                correo_direccion=datos['correo_direccion'],
                jefe_departamento=datos.get('jefe_departamento'),
                correo_jefe_departamento=datos.get('correo_jefe_departamento'),
                categoria_formativa=datos['categoria_formativa'],
                cursos_especificos=datos['cursos_especificos'],
                confirmado=True
            )
            participante.save()
            participantes_creados.append(participante)
            print(f"  ✓ Creado: {participante.nombre} {participante.apellido_paterno}")
            
        except Exception as e:
            print(f"  ✗ Error creando {datos['nombre']}: {str(e)}")
    
    print(f"Participantes creados: {len(participantes_creados)}")
    return participantes_creados

def crear_reuniones_capacitacion():
    """Crear reuniones de capacitación de ejemplo"""
    
    reuniones_datos = [
        {
            'titulo': 'Curso: Introducción a la Ciencia de Datos',
            'descripcion': 'Curso fundamental sobre análisis de datos, estadística aplicada y herramientas de visualización para docentes del TecNM.',
            'tipo': 'CURSO_CAPACITACION',
            'estado': 'FINALIZADA',
            'modalidad': 'VIRTUAL',
            'fecha_inicio': timezone.now() - timedelta(days=30),
            'fecha_fin': timezone.now() - timedelta(days=28),
            'sede': 'Plataforma Virtual TecNM',
            'enlace_videollamada': 'https://meet.tecnm.mx/ciencia-datos-01',
            'organizador_principal': 'Dr. Miguel Rodríguez Pérez',
            'participantes_esperados': 25
        },
        {
            'titulo': 'Taller: Inteligencia Artificial en la Educación',
            'descripcion': 'Taller práctico sobre la implementación de herramientas de IA en procesos educativos y administrativos.',
            'tipo': 'TALLER',
            'estado': 'PLANIFICADA',
            'modalidad': 'HIBRIDA',
            'fecha_inicio': timezone.now() + timedelta(days=15),
            'fecha_fin': timezone.now() + timedelta(days=17),
            'sede': 'Instituto Tecnológico de Guadalajara',
            'direccion_fisica': 'Av. Revolución 1500, Col. Olímpica, 44430 Guadalajara, Jal.',
            'enlace_videollamada': 'https://meet.tecnm.mx/ia-educacion',
            'organizador_principal': 'Carlos Ruiz Fernández',
            'participantes_esperados': 40
        },
        {
            'título': 'Seminario: Liderazgo y Gestión Estratégica',
            'descripcion': 'Seminario dirigido a personal directivo sobre técnicas modernas de liderazgo y planeación estratégica institucional.',
            'tipo': 'SEMINARIO',
            'estado': 'EN_CURSO',
            'modalidad': 'PRESENCIAL',
            'fecha_inicio': timezone.now() - timedelta(days=1),
            'fecha_fin': timezone.now() + timedelta(days=2),
            'sede': 'Instituto Tecnológico de Toluca',
            'direccion_fisica': 'Av. Instituto Tecnológico s/n, Col. Agrícola Bellavista, 52149 Metepec, Méx.',
            'organizador_principal': 'Roberto Hernández López',
            'participantes_esperados': 15
        }
    ]
    
    print("Creando reuniones de capacitación...")
    reuniones_creadas = []
    
    for datos in reuniones_datos:
        try:
            reunion = ReunionNacional(
                titulo=datos['titulo'],
                descripcion=datos['descripcion'],
                tipo=datos['tipo'],
                estado=datos['estado'],
                modalidad=datos['modalidad'],
                fecha_inicio=datos['fecha_inicio'],
                fecha_fin=datos['fecha_fin'],
                sede=datos['sede'],
                enlace_videollamada=datos.get('enlace_videollamada'),
                direccion_fisica=datos.get('direccion_fisica'),
                organizador_principal=datos['organizador_principal'],
                participantes_esperados=datos['participantes_esperados'],
                participantes=[],
                agenda=[],
                documentos=[]
            )
            reunion.save()
            reuniones_creadas.append(reunion)
            print(f"  ✓ Creada: {reunion.titulo}")
            
        except Exception as e:
            print(f"  ✗ Error creando reunión: {str(e)}")
    
    print(f"Reuniones creadas: {len(reuniones_creadas)}")
    return reuniones_creadas

def main():
    """Función principal"""
    print("=== Creando datos de prueba para el Sistema de Capacitaciones TecNM ===")
    print()
    
    try:
        # Crear participantes
        participantes = crear_participantes_ejemplo()
        print()
        
        # Crear reuniones
        reuniones = crear_reuniones_capacitacion()
        print()
        
        print("=== Datos de prueba creados exitosamente ===")
        print(f"Participantes: {len(participantes)}")
        print(f"Reuniones: {len(reuniones)}")
        print()
        print("Puedes acceder al dashboard en:")
        print("http://127.0.0.1:8000/mi_aplication/capacitaciones/")
        
    except Exception as e:
        print(f"Error durante la creación de datos: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()