#!/usr/bin/env python3
"""
Script para generar datos fake para SQLite/MySQL
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

# Importar modelos SQL
from mi_aplication.models_sql import (
    ReunionNacional, Acuerdo, Participante, Documento,
    ParticipanteReunion, AgendaItem, SeguimientoAcuerdo
)

def generar_datos_fake_sql():
    """Generar datos fake para SQL"""
    
    print("🗑️ Limpiando datos existentes...")
    SeguimientoAcuerdo.objects.all().delete()
    ParticipanteReunion.objects.all().delete()
    AgendaItem.objects.all().delete()
    Documento.objects.all().delete()
    Acuerdo.objects.all().delete()
    ReunionNacional.objects.all().delete()
    Participante.objects.all().delete()
    
    print("📝 Generando datos fake para SQL...")
    
    # ============================================================================
    # GENERAR PARTICIPANTES
    # ============================================================================
    print("👥 Generando participantes...")
    
    participantes_data = [
        {
            'nombre': 'Juan Carlos', 'apellido_paterno': 'García', 'apellido_materno': 'Rodríguez',
            'email': 'juan.garcia@itq.edu.mx', 'telefono': '+52 442 123 4567',
            'instituto': 'IT Querétaro', 'departamento': 'Dirección General',
            'tipo_participante': 'DIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'María Elena', 'apellido_paterno': 'López', 'apellido_materno': 'Martínez',
            'email': 'maria.lopez@itc.edu.mx', 'telefono': '+52 461 234 5678',
            'instituto': 'IT Celaya', 'departamento': 'Dirección General',
            'tipo_participante': 'DIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'Roberto Carlos', 'apellido_paterno': 'Hernández', 'apellido_materno': 'González',
            'email': 'roberto.hernandez@itm.edu.mx', 'telefono': '+52 55 345 6789',
            'instituto': 'IT Morelia', 'departamento': 'Dirección General',
            'tipo_participante': 'DIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'Ana Patricia', 'apellido_paterno': 'Sánchez', 'apellido_materno': 'Díaz',
            'email': 'ana.sanchez@itg.edu.mx', 'telefono': '+52 33 456 7890',
            'instituto': 'IT Guadalajara', 'departamento': 'Dirección General',
            'tipo_participante': 'DIRECTOR', 'confirmado': False
        },
        {
            'nombre': 'Carlos Alberto', 'apellido_paterno': 'Ramírez', 'apellido_materno': 'Vargas',
            'email': 'carlos.ramirez@itp.edu.mx', 'telefono': '+52 81 567 8901',
            'instituto': 'IT Puebla', 'departamento': 'Dirección General',
            'tipo_participante': 'DIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'Laura Beatriz', 'apellido_paterno': 'Morales', 'apellido_materno': 'Castro',
            'email': 'laura.morales@itq.edu.mx', 'telefono': '+52 442 678 9012',
            'instituto': 'IT Querétaro', 'departamento': 'Subdirección Académica',
            'tipo_participante': 'SUBDIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'Miguel Ángel', 'apellido_paterno': 'Torres', 'apellido_materno': 'Ruiz',
            'email': 'miguel.torres@itc.edu.mx', 'telefono': '+52 461 789 0123',
            'instituto': 'IT Celaya', 'departamento': 'Subdirección Académica',
            'tipo_participante': 'SUBDIRECTOR', 'confirmado': True
        },
        {
            'nombre': 'Ricardo José', 'apellido_paterno': 'Mendoza', 'apellido_materno': 'Silva',
            'email': 'ricardo.mendoza@itq.edu.mx', 'telefono': '+52 442 901 2345',
            'instituto': 'IT Querétaro', 'departamento': 'Coordinación de Posgrado',
            'tipo_participante': 'COORDINADOR', 'confirmado': True
        },
        {
            'nombre': 'Dr. Alejandro', 'apellido_paterno': 'Pérez', 'apellido_materno': 'Gutiérrez',
            'email': 'alejandro.perez@itq.edu.mx', 'telefono': '+52 442 234 5678',
            'instituto': 'IT Querétaro', 'departamento': 'Ingeniería en Sistemas',
            'tipo_participante': 'DOCENTE', 'confirmado': True
        },
        {
            'nombre': 'Lic. Gabriela', 'apellido_paterno': 'Martínez', 'apellido_materno': 'López',
            'email': 'gabriela.martinez@itq.edu.mx', 'telefono': '+52 442 567 8901',
            'instituto': 'IT Querétaro', 'departamento': 'Recursos Humanos',
            'tipo_participante': 'ADMINISTRATIVO', 'confirmado': True
        }
    ]
    
    participantes_creados = []
    for data in participantes_data:
        participante = Participante.objects.create(**data)
        participantes_creados.append(participante)
        print(f"✅ Participante creado: {participante.nombre} {participante.apellido_paterno}")
    
    # ============================================================================
    # GENERAR REUNIONES NACIONALES
    # ============================================================================
    print("\n🏢 Generando reuniones nacionales...")
    
    reuniones_data = [
        {
            'titulo': 'Reunión Nacional de Posgrado y Desarrollo 2024',
            'tipo': 'RNPD',
            'fecha_inicio': datetime(2024, 12, 5, 8, 30),
            'fecha_fin': datetime(2024, 12, 5, 17, 0),
            'sede': 'Instituto Tecnológico de Querétaro',
            'modalidad': 'HIBRIDA',
            'enlace_videollamada': 'https://meet.google.com/abc-defg-hij',
            'direccion_fisica': 'Av. Tecnológico s/n, Centro, 76000 Santiago de Querétaro, Qro.',
            'estado': 'PLANIFICADA',
            'organizador_principal': 'Dr. Juan Carlos García Rodríguez',
            'descripcion': 'Reunión nacional para fortalecer los programas de posgrado y desarrollo tecnológico en los institutos tecnológicos del TecNM.',
            'objetivos': 'Fortalecer la colaboración entre institutos, compartir mejores prácticas y establecer acuerdos para el desarrollo de nuevos programas de posgrado.',
            'participantes_esperados': 80,
            'presupuesto_asignado': 150000.00
        },
        {
            'titulo': 'Reunión Nacional de Subdirectores Académicos 2024',
            'tipo': 'RNSA',
            'fecha_inicio': datetime(2024, 11, 15, 9, 0),
            'fecha_fin': datetime(2024, 11, 16, 16, 0),
            'sede': 'Instituto Tecnológico de Celaya',
            'modalidad': 'PRESENCIAL',
            'direccion_fisica': 'Av. Tecnológico y García Cubas s/n, 38010 Celaya, Gto.',
            'estado': 'FINALIZADA',
            'organizador_principal': 'Dra. María Elena López Martínez',
            'descripcion': 'Reunión nacional de subdirectores académicos para coordinar estrategias educativas.',
            'objetivos': 'Establecer líneas de investigación prioritarias, fomentar la colaboración interinstitucional y definir estrategias de innovación.',
            'participantes_esperados': 120,
            'presupuesto_asignado': 200000.00
        },
        {
            'titulo': 'Reunión Nacional de Vinculación y Extensión 2024',
            'tipo': 'RNVE',
            'fecha_inicio': datetime(2024, 10, 20, 8, 0),
            'fecha_fin': datetime(2024, 10, 20, 18, 0),
            'sede': 'Instituto Tecnológico de Morelia',
            'modalidad': 'HIBRIDA',
            'enlace_videollamada': 'https://meet.google.com/xyz-uvw-rst',
            'direccion_fisica': 'Av. Tecnológico 1500, Lomas de Santiaguito, 58120 Morelia, Mich.',
            'estado': 'FINALIZADA',
            'organizador_principal': 'Dr. Roberto Carlos Hernández González',
            'descripcion': 'Reunión nacional para fortalecer la vinculación con el sector productivo y la extensión de servicios.',
            'objetivos': 'Establecer alianzas estratégicas con empresas, definir programas de extensión y compartir experiencias exitosas de vinculación.',
            'participantes_esperados': 90,
            'presupuesto_asignado': 180000.00
        }
    ]
    
    reuniones_creadas = []
    for i, data in enumerate(reuniones_data):
        reunion = ReunionNacional.objects.create(**data)
        reuniones_creadas.append(reunion)
        print(f"✅ Reunión creada: {reunion.titulo}")
        
        # Agregar participantes a la reunión
        participantes_reunion = random.sample(participantes_creados, random.randint(5, 8))
        for participante in participantes_reunion:
            ParticipanteReunion.objects.create(
                reunion=reunion,
                participante=participante,
                confirmado=random.choice([True, True, True, False]),
                observaciones=random.choice([
                    'Participante confirmado',
                    'Pendiente de confirmación',
                    'Asistencia confirmada',
                    'Por confirmar'
                ])
            )
        
        # Agregar agenda
        agenda_items = [
            {
                'titulo': 'Registro y Bienvenida',
                'descripcion': 'Registro de participantes y palabras de bienvenida',
                'hora_inicio': '08:30',
                'hora_fin': '09:00',
                'responsable': reunion.organizador_principal,
                'tipo_actividad': 'PRESENTACION',
                'orden': 1
            },
            {
                'titulo': 'Presentación de Objetivos',
                'descripcion': 'Exposición de los objetivos y agenda de la reunión',
                'hora_inicio': '09:00',
                'hora_fin': '09:45',
                'responsable': reunion.organizador_principal,
                'tipo_actividad': 'PRESENTACION',
                'orden': 2
            },
            {
                'titulo': 'Panel de Expertos',
                'descripcion': 'Panel con expertos del sector para discutir temas relevantes',
                'hora_inicio': '10:00',
                'hora_fin': '11:30',
                'responsable': 'Panel de Expertos',
                'tipo_actividad': 'DISCUSION',
                'orden': 3
            },
            {
                'titulo': 'Receso',
                'descripcion': 'Pausa para café y networking',
                'hora_inicio': '11:30',
                'hora_fin': '12:00',
                'responsable': 'N/A',
                'tipo_actividad': 'RECESO',
                'orden': 4
            },
            {
                'titulo': 'Mesas de Trabajo',
                'descripcion': 'Sesiones de trabajo en grupos para abordar temas específicos',
                'hora_inicio': '12:00',
                'hora_fin': '14:00',
                'responsable': 'Coordinadores de Mesa',
                'tipo_actividad': 'TRABAJO_GRUPO',
                'orden': 5
            }
        ]
        
        for item_data in agenda_items:
            item_data['reunion'] = reunion
            AgendaItem.objects.create(**item_data)
        
        # Agregar documentos
        documentos_reunion = [
            {
                'titulo': f'Agenda de la {reunion.titulo}',
                'descripcion': f'Agenda oficial de la {reunion.titulo}',
                'tipo': 'AGENDA',
                'url': f'https://drive.google.com/file/d/agenda_{i+1}/view',
                'formato': 'pdf',
                'tamaño': random.randint(500000, 2000000),
                'version': '1.0',
                'subido_por': reunion.organizador_principal,
                'reunion': reunion
            },
            {
                'titulo': f'Presentación de Apertura - {reunion.titulo}',
                'descripcion': f'Presentación de apertura de la {reunion.titulo}',
                'tipo': 'PRESENTACION',
                'url': f'https://drive.google.com/file/d/presentacion_{i+1}/view',
                'formato': 'pptx',
                'tamaño': random.randint(2000000, 5000000),
                'version': '1.0',
                'subido_por': reunion.organizador_principal,
                'reunion': reunion
            }
        ]
        
        for doc_data in documentos_reunion:
            Documento.objects.create(**doc_data)
    
    # ============================================================================
    # GENERAR ACUERDOS
    # ============================================================================
    print("\n📋 Generando acuerdos...")
    
    acuerdos_data = [
        {
            'titulo': 'Implementación de nuevos programas de posgrado',
            'descripcion': 'Se acuerda implementar 3 nuevos programas de posgrado en áreas estratégicas: Maestría en Inteligencia Artificial, Maestría en Energías Renovables y Doctorado en Ingeniería de Sistemas.',
            'categoria': 'ACADEMICA',
            'estado': 'EN_PROCESO',
            'prioridad': 'ALTA',
            'reunion': reuniones_creadas[0],
            'responsable': 'Lic. Roberto Martínez Castro',
            'fecha_limite': datetime(2025, 6, 30, 23, 59, 59)
        },
        {
            'titulo': 'Establecimiento de alianzas estratégicas con empresas',
            'descripcion': 'Se acuerda establecer alianzas estratégicas con 10 empresas líderes en el sector tecnológico para fortalecer la vinculación y el desarrollo de proyectos conjuntos.',
            'categoria': 'VINCULACION',
            'estado': 'PENDIENTE',
            'prioridad': 'MEDIA',
            'reunion': reuniones_creadas[2],
            'responsable': 'Dra. María Elena López Martínez',
            'fecha_limite': datetime(2025, 3, 31, 23, 59, 59)
        },
        {
            'titulo': 'Modernización de la infraestructura tecnológica',
            'descripcion': 'Se acuerda modernizar la infraestructura tecnológica de todos los institutos tecnológicos, incluyendo actualización de equipos de cómputo, redes y sistemas de información.',
            'categoria': 'INFRAESTRUCTURA',
            'estado': 'EN_PROCESO',
            'prioridad': 'ALTA',
            'reunion': reuniones_creadas[0],
            'responsable': 'Dr. Carlos Alberto Ramírez Vargas',
            'fecha_limite': datetime(2025, 12, 31, 23, 59, 59)
        }
    ]
    
    acuerdos_creados = []
    for i, data in enumerate(acuerdos_data):
        acuerdo = Acuerdo.objects.create(**data)
        acuerdos_creados.append(acuerdo)
        print(f"✅ Acuerdo creado: {acuerdo.titulo}")
        
        # Agregar seguimientos
        if acuerdo.estado in ['EN_PROCESO', 'COMPLETADO']:
            SeguimientoAcuerdo.objects.create(
                acuerdo=acuerdo,
                estado_anterior='PENDIENTE',
                estado_nuevo='EN_PROCESO',
                porcentaje_avance=10,
                observaciones='Acuerdo aprobado en reunión. Iniciando proceso de implementación.',
                responsable=acuerdo.responsable
            )
            
            if acuerdo.estado == 'EN_PROCESO':
                SeguimientoAcuerdo.objects.create(
                    acuerdo=acuerdo,
                    estado_anterior='EN_PROCESO',
                    estado_nuevo='EN_PROCESO',
                    porcentaje_avance=random.randint(25, 75),
                    observaciones='Proceso de implementación en curso. Avances significativos realizados.',
                    responsable=acuerdo.responsable
                )
        
        # Agregar documentos al acuerdo
        Documento.objects.create(
            titulo=f'Propuesta de {acuerdo.titulo}',
            descripcion=f'Propuesta detallada para la implementación del acuerdo: {acuerdo.titulo}',
            tipo='PRESENTACION',
            url=f'https://drive.google.com/file/d/propuesta_acuerdo_{i+1}/view',
            formato='pptx',
            tamaño=random.randint(2000000, 8000000),
            version='1.0',
            subido_por=acuerdo.responsable,
            acuerdo=acuerdo
        )
    
    # ============================================================================
    # GENERAR DOCUMENTOS INDEPENDIENTES
    # ============================================================================
    print("\n📄 Generando documentos independientes...")
    
    documentos_independientes = [
        {
            'titulo': 'Manual de Procedimientos del TecNM',
            'descripcion': 'Manual actualizado de procedimientos administrativos y académicos del TecNM',
            'tipo': 'CIRCULAR',
            'url': 'https://drive.google.com/file/d/manual_procedimientos_2024/view',
            'formato': 'pdf',
            'tamaño': 5000000,
            'version': '2024.1',
            'subido_por': 'Dr. Juan Carlos García Rodríguez'
        },
        {
            'titulo': 'Estadísticas de Egresados 2024',
            'descripcion': 'Reporte estadístico de egresados de todos los institutos tecnológicos del TecNM',
            'tipo': 'ACTA',
            'url': 'https://drive.google.com/file/d/estadisticas_egresados_2024/view',
            'formato': 'xlsx',
            'tamaño': 2500000,
            'version': '1.0',
            'subido_por': 'Lic. Gabriela Martínez López'
        },
        {
            'titulo': 'Guía de Mejores Prácticas en Investigación',
            'descripcion': 'Guía actualizada de mejores prácticas en investigación para docentes del TecNM',
            'tipo': 'MEMORANDUM',
            'url': 'https://drive.google.com/file/d/guia_investigacion_2024/view',
            'formato': 'pdf',
            'tamaño': 3500000,
            'version': '2024.2',
            'subido_por': 'Dr. Alejandro Pérez Gutiérrez'
        }
    ]
    
    for data in documentos_independientes:
        documento = Documento.objects.create(**data)
        print(f"✅ Documento creado: {documento.titulo}")
    
    print(f"\n🎉 ¡Datos fake para SQL generados exitosamente!")
    print(f"📊 Resumen:")
    print(f"   • {len(participantes_creados)} participantes")
    print(f"   • {len(reuniones_creadas)} reuniones nacionales")
    print(f"   • {len(acuerdos_creados)} acuerdos")
    print(f"   • {len(documentos_independientes)} documentos independientes")
    print(f"   • Relaciones muchos a muchos establecidas")
    print(f"   • Seguimientos y documentos asociados")

if __name__ == '__main__':
    try:
        generar_datos_fake_sql()
    except Exception as e:
        print(f"❌ Error al generar datos: {e}")
        import traceback
        traceback.print_exc()
