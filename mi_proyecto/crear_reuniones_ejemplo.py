#!/usr/bin/env python
"""
Script para generar reuniones de ejemplo si no hay ninguna en el sistema
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import ReunionNacional
from mi_aplication.constants import TIPOS_REUNION, ESTADOS_REUNION, MODALIDADES_REUNION
from django.utils import timezone

def crear_reuniones_ejemplo():
    """Crea reuniones de ejemplo si no hay ninguna"""
    
    # Verificar si ya hay reuniones
    total_reuniones = ReunionNacional.objects.count()
    
    if total_reuniones > 0:
        print(f"✓ Ya existen {total_reuniones} reuniones en el sistema")
        return
    
    print("=" * 80)
    print("CREANDO REUNIONES DE EJEMPLO")
    print("=" * 80)
    
    reuniones_ejemplo = [
        {
            'titulo': 'Reunión Nacional de Directores 2025',
            'tipo': 'DIRECTORES',
            'estado': 'PLANIFICADA',
            'fecha_inicio': timezone.now() + timedelta(days=30),
            'fecha_fin': timezone.now() + timedelta(days=32),
            'sede': 'Tecnológico Nacional de México - Sede Central',
            'modalidad': 'HIBRIDA',
            'descripcion': 'Reunión anual de directores de todos los institutos del TecNM',
            'objetivos': 'Revisar estrategias, compartir mejores prácticas y definir objetivos institucionales',
            'participantes_esperados': 150,
            'organizador_principal': 'Dirección General del TecNM',
        },
        {
            'titulo': 'Congreso de Investigación y Desarrollo Tecnológico',
            'tipo': 'ACADEMICA',
            'estado': 'PLANIFICADA',
            'fecha_inicio': timezone.now() + timedelta(days=60),
            'fecha_fin': timezone.now() + timedelta(days=63),
            'sede': 'Instituto Tecnológico de Monterrey',
            'modalidad': 'PRESENCIAL',
            'descripcion': 'Congreso anual para presentar proyectos de investigación',
            'objetivos': 'Fomentar la investigación y el desarrollo tecnológico en el TecNM',
            'participantes_esperados': 300,
            'organizador_principal': 'Subdirección de Investigación',
            'presupuesto_asignado': 500000.0,
        },
        {
            'titulo': 'Taller de Capacitación Docente en Metodologías Activas',
            'tipo': 'CAPACITACION',
            'estado': 'PLANIFICADA',
            'fecha_inicio': timezone.now() + timedelta(days=15),
            'fecha_fin': timezone.now() + timedelta(days=15),
            'sede': 'Instituto Tecnológico de Tijuana',
            'modalidad': 'VIRTUAL',
            'descripcion': 'Capacitación en metodologías activas de enseñanza',
            'objetivos': 'Mejorar las competencias docentes en metodologías innovadoras',
            'participantes_esperados': 80,
            'enlace_videollamada': 'https://meet.google.com/ejemplo-reunion',
            'organizador_principal': 'Dirección de Desarrollo Académico',
        },
        {
            'titulo': 'Reunión de Seguimiento de Acuerdos 2024',
            'tipo': 'SEGUIMIENTO',
            'estado': 'EN_CURSO',
            'fecha_inicio': timezone.now() - timedelta(days=2),
            'fecha_fin': timezone.now() + timedelta(days=1),
            'sede': 'Tecnológico Nacional de México - Virtual',
            'modalidad': 'VIRTUAL',
            'descripcion': 'Seguimiento a los acuerdos tomados en el año 2024',
            'objetivos': 'Evaluar cumplimiento de acuerdos y definir acciones correctivas',
            'participantes_esperados': 50,
            'enlace_videollamada': 'https://zoom.us/j/ejemplo',
            'organizador_principal': 'Secretaría Técnica',
        },
        {
            'titulo': 'Foro de Vinculación con el Sector Productivo',
            'tipo': 'OTRA',
            'estado': 'PLANIFICADA',
            'fecha_inicio': timezone.now() + timedelta(days=45),
            'fecha_fin': timezone.now() + timedelta(days=46),
            'sede': 'Instituto Tecnológico de Guadalajara',
            'modalidad': 'PRESENCIAL',
            'descripcion': 'Foro para fortalecer la vinculación con empresas y sector productivo',
            'objetivos': 'Establecer convenios de colaboración y oportunidades de prácticas',
            'participantes_esperados': 200,
            'organizador_principal': 'Dirección de Vinculación',
            'presupuesto_asignado': 300000.0,
        },
        {
            'titulo': 'Reunión Extraordinaria de Coordinadores Académicos',
            'tipo': 'ACADEMICA',
            'estado': 'FINALIZADA',
            'fecha_inicio': timezone.now() - timedelta(days=30),
            'fecha_fin': timezone.now() - timedelta(days=30),
            'sede': 'Instituto Tecnológico de Querétaro',
            'modalidad': 'HIBRIDA',
            'descripcion': 'Reunión extraordinaria para revisar programas académicos',
            'objetivos': 'Actualizar programas de estudio y compartir experiencias',
            'participantes_esperados': 100,
            'organizador_principal': 'Coordinación General Académica',
        },
    ]
    
    creadas = 0
    errores = 0
    
    for i, datos in enumerate(reuniones_ejemplo, 1):
        try:
            print(f"\n[{i}/{len(reuniones_ejemplo)}] Creando: {datos['titulo']}")
            
            reunion = ReunionNacional(**datos)
            reunion.save()
            
            creadas += 1
            print(f"  ✓ Creada exitosamente")
            
        except Exception as e:
            errores += 1
            print(f"  ✗ Error: {str(e)}")
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Reuniones creadas: {creadas}")
    print(f"Errores: {errores}")
    print("=" * 80)
    
    if creadas > 0:
        print("\n✓ Sistema listo con reuniones de ejemplo")
    else:
        print("\n✗ No se pudieron crear reuniones de ejemplo")

if __name__ == '__main__':
    try:
        crear_reuniones_ejemplo()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
