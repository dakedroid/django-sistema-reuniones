#!/usr/bin/env python3
"""
Script para generar datos fake mejorados para el sistema de reuniones nacionales TecNM
Con información más completa y realista en todas las colecciones
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import ReunionNacional, Acuerdo, Participante, Documento
from bson import ObjectId

def generar_datos_fake_mejorados():
    """Generar datos fake mejorados y más completos"""
    
    print("🗑️ Limpiando colecciones existentes...")
    ReunionNacional.objects.delete()
    Acuerdo.objects.delete()
    Participante.objects.delete()
    Documento.objects.delete()
    
    print("📝 Generando datos fake mejorados...")
    
    # ============================================================================
    # GENERAR PARTICIPANTES (más completos)
    # ============================================================================
    print("👥 Generando participantes...")
    
    participantes_data = [
        # Directores
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
        
        # Subdirectores
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
            'nombre': 'Patricia Guadalupe', 'apellido_paterno': 'Flores', 'apellido_materno': 'Jiménez',
            'email': 'patricia.flores@itm.edu.mx', 'telefono': '+52 55 890 1234',
            'instituto': 'IT Morelia', 'departamento': 'Subdirección Académica',
            'tipo_participante': 'SUBDIRECTOR', 'confirmado': False
        },
        
        # Coordinadores
        {
            'nombre': 'Ricardo José', 'apellido_paterno': 'Mendoza', 'apellido_materno': 'Silva',
            'email': 'ricardo.mendoza@itq.edu.mx', 'telefono': '+52 442 901 2345',
            'instituto': 'IT Querétaro', 'departamento': 'Coordinación de Posgrado',
            'tipo_participante': 'COORDINADOR', 'confirmado': True
        },
        {
            'nombre': 'Sandra Elizabeth', 'apellido_paterno': 'Vega', 'apellido_materno': 'Ortiz',
            'email': 'sandra.vega@itc.edu.mx', 'telefono': '+52 461 012 3456',
            'instituto': 'IT Celaya', 'departamento': 'Coordinación de Posgrado',
            'tipo_participante': 'COORDINADOR', 'confirmado': True
        },
        {
            'nombre': 'Fernando Javier', 'apellido_paterno': 'Cruz', 'apellido_materno': 'Mendoza',
            'email': 'fernando.cruz@itm.edu.mx', 'telefono': '+52 55 123 4567',
            'instituto': 'IT Morelia', 'departamento': 'Coordinación de Posgrado',
            'tipo_participante': 'COORDINADOR', 'confirmado': True
        },
        
        # Docentes
        {
            'nombre': 'Dr. Alejandro', 'apellido_paterno': 'Pérez', 'apellido_materno': 'Gutiérrez',
            'email': 'alejandro.perez@itq.edu.mx', 'telefono': '+52 442 234 5678',
            'instituto': 'IT Querétaro', 'departamento': 'Ingeniería en Sistemas',
            'tipo_participante': 'DOCENTE', 'confirmado': True
        },
        {
            'nombre': 'Dra. Carmen', 'apellido_paterno': 'Reyes', 'apellido_materno': 'Navarro',
            'email': 'carmen.reyes@itc.edu.mx', 'telefono': '+52 461 345 6789',
            'instituto': 'IT Celaya', 'departamento': 'Ingeniería Industrial',
            'tipo_participante': 'DOCENTE', 'confirmado': True
        },
        {
            'nombre': 'Dr. Luis Manuel', 'apellido_paterno': 'Díaz', 'apellido_materno': 'Moreno',
            'email': 'luis.diaz@itm.edu.mx', 'telefono': '+52 55 456 7890',
            'instituto': 'IT Morelia', 'departamento': 'Ingeniería Mecánica',
            'tipo_participante': 'DOCENTE', 'confirmado': False
        },
        
        # Administrativos
        {
            'nombre': 'Lic. Gabriela', 'apellido_paterno': 'Martínez', 'apellido_materno': 'López',
            'email': 'gabriela.martinez@itq.edu.mx', 'telefono': '+52 442 567 8901',
            'instituto': 'IT Querétaro', 'departamento': 'Recursos Humanos',
            'tipo_participante': 'ADMINISTRATIVO', 'confirmado': True
        },
        {
            'nombre': 'Lic. José Luis', 'apellido_paterno': 'González', 'apellido_materno': 'Herrera',
            'email': 'jose.gonzalez@itc.edu.mx', 'telefono': '+52 461 678 9012',
            'instituto': 'IT Celaya', 'departamento': 'Finanzas',
            'tipo_participante': 'ADMINISTRATIVO', 'confirmado': True
        },
        
        # Invitados
        {
            'nombre': 'Ing. Roberto', 'apellido_paterno': 'Martínez', 'apellido_materno': 'Castro',
            'email': 'roberto.martinez@conacyt.mx', 'telefono': '+52 55 789 0123',
            'instituto': 'CONACYT', 'departamento': 'Dirección de Posgrado',
            'tipo_participante': 'INVITADO', 'confirmado': True
        },
        {
            'nombre': 'Mtra. Claudia', 'apellido_paterno': 'Fernández', 'apellido_materno': 'Ríos',
            'email': 'claudia.fernandez@sep.gob.mx', 'telefono': '+52 55 890 1234',
            'instituto': 'SEP', 'departamento': 'Subsecretaría de Educación Superior',
            'tipo_participante': 'INVITADO', 'confirmado': True
        }
    ]
    
    participantes_creados = []
    for data in participantes_data:
        participante = Participante(**data)
        participante.save()
        participantes_creados.append(participante)
        print(f"✅ Participante creado: {participante.nombre} {participante.apellido_paterno}")
    
    # ============================================================================
    # GENERAR REUNIONES NACIONALES (más completas)
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
        },
        {
            'titulo': 'Reunión Nacional de Calidad y Acreditación 2024',
            'tipo': 'RNCA',
            'fecha_inicio': datetime(2024, 9, 25, 9, 30),
            'fecha_fin': datetime(2024, 9, 25, 16, 30),
            'sede': 'Instituto Tecnológico de Guadalajara',
            'modalidad': 'PRESENCIAL',
            'direccion_fisica': 'Av. Revolución 1500, 44840 Guadalajara, Jal.',
            'estado': 'FINALIZADA',
            'organizador_principal': 'Dra. Ana Patricia Sánchez Díaz',
            'descripcion': 'Reunión nacional para optimizar la administración y gestión financiera de los institutos tecnológicos.',
            'objetivos': 'Compartir mejores prácticas administrativas, optimizar procesos financieros y establecer estándares de gestión.',
            'participantes_esperados': 60,
            'presupuesto_asignado': 120000.00
        },
        {
            'titulo': 'Reunión Nacional de Tecnologías de la Información 2024',
            'tipo': 'OTRA',
            'fecha_inicio': datetime(2025, 1, 15, 8, 0),
            'fecha_fin': datetime(2025, 1, 16, 17, 0),
            'sede': 'Instituto Tecnológico de Puebla',
            'modalidad': 'HIBRIDA',
            'enlace_videollamada': 'https://meet.google.com/mno-pqr-stu',
            'direccion_fisica': 'Av. Tecnológico 420, 72220 Puebla, Pue.',
            'estado': 'PLANIFICADA',
            'organizador_principal': 'Dr. Carlos Alberto Ramírez Vargas',
            'descripcion': 'Reunión nacional para discutir las tendencias en tecnologías de la información y su aplicación en la educación.',
            'objetivos': 'Actualizar conocimientos en TI, establecer estándares tecnológicos y promover la innovación digital.',
            'participantes_esperados': 100,
            'presupuesto_asignado': 160000.00
        }
    ]
    
    reuniones_creadas = []
    for i, data in enumerate(reuniones_data):
        reunion = ReunionNacional(**data)
        reunion.save()
        reuniones_creadas.append(reunion)
        print(f"✅ Reunión creada: {reunion.titulo}")
        
        # Agregar participantes embebidos a cada reunión
        participantes_reunion = random.sample(participantes_creados, random.randint(8, 15))
        for participante in participantes_reunion:
            from mi_aplication.models import ParticipanteEmbebido
            participante_embebido = ParticipanteEmbebido(
                nombre=participante.nombre,
                apellido_paterno=participante.apellido_paterno,
                apellido_materno=participante.apellido_materno,
                email=participante.email,
                telefono=participante.telefono,
                instituto=participante.instituto,
                departamento=participante.departamento,
                tipo_participante=participante.tipo_participante,
                confirmado=random.choice([True, True, True, False]),  # 75% confirmados
                observaciones=random.choice([
                    'Participante confirmado',
                    'Pendiente de confirmación',
                    'Asistencia confirmada',
                    'Por confirmar'
                ])
            )
            reunion.participantes.append(participante_embebido)
        
        # Agregar agenda embebida
        from mi_aplication.models import AgendaEmbebido
        agenda_items = [
            AgendaEmbebido(
                titulo='Registro y Bienvenida',
                descripcion='Registro de participantes y palabras de bienvenida',
                hora_inicio='08:30',
                hora_fin='09:00',
                responsable=reunion.organizador_principal,
                tipo_actividad='PRESENTACION'
            ),
            AgendaEmbebido(
                titulo='Presentación de Objetivos',
                descripcion='Exposición de los objetivos y agenda de la reunión',
                hora_inicio='09:00',
                hora_fin='09:45',
                responsable=reunion.organizador_principal,
                tipo_actividad='PRESENTACION'
            ),
            AgendaEmbebido(
                titulo='Panel de Expertos',
                descripcion='Panel con expertos del sector para discutir temas relevantes',
                hora_inicio='10:00',
                hora_fin='11:30',
                responsable='Panel de Expertos',
                tipo_actividad='DISCUSION'
            ),
            AgendaEmbebido(
                titulo='Receso',
                descripcion='Pausa para café y networking',
                hora_inicio='11:30',
                hora_fin='12:00',
                responsable='N/A',
                tipo_actividad='RECESO'
            ),
            AgendaEmbebido(
                titulo='Mesas de Trabajo',
                descripcion='Sesiones de trabajo en grupos para abordar temas específicos',
                hora_inicio='12:00',
                hora_fin='14:00',
                responsable='Coordinadores de Mesa',
                tipo_actividad='TRABAJO_GRUPO'
            ),
            AgendaEmbebido(
                titulo='Comida',
                descripcion='Almuerzo de trabajo',
                hora_inicio='14:00',
                hora_fin='15:00',
                responsable='N/A',
                tipo_actividad='RECESO'
            ),
            AgendaEmbebido(
                titulo='Presentación de Resultados',
                descripcion='Presentación de los resultados de las mesas de trabajo',
                hora_inicio='15:00',
                hora_fin='16:30',
                responsable='Relatores',
                tipo_actividad='PRESENTACION'
            ),
            AgendaEmbebido(
                titulo='Cierre y Acuerdos',
                descripcion='Resumen de acuerdos y cierre de la reunión',
                hora_inicio='16:30',
                hora_fin='17:00',
                responsable=reunion.organizador_principal,
                tipo_actividad='DISCUSION'
            )
        ]
        reunion.agenda = agenda_items
        
        # Agregar documentos embebidos
        from mi_aplication.models import DocumentoEmbebido
        documentos_reunion = [
            DocumentoEmbebido(
                titulo=f'Agenda de la {reunion.titulo}',
                descripcion=f'Agenda oficial de la {reunion.titulo}',
                tipo='AGENDA',
                url=f'https://drive.google.com/file/d/agenda_{i+1}/view',
                formato='pdf',
                tamaño=random.randint(500000, 2000000),
                version='1.0',
                subido_por=reunion.organizador_principal,
                fecha_subida=reunion.fecha_inicio - timedelta(days=7)
            ),
            DocumentoEmbebido(
                titulo=f'Presentación de Apertura - {reunion.titulo}',
                descripcion=f'Presentación de apertura de la {reunion.titulo}',
                tipo='PRESENTACION',
                url=f'https://drive.google.com/file/d/presentacion_{i+1}/view',
                formato='pptx',
                tamaño=random.randint(2000000, 5000000),
                version='1.0',
                subido_por=reunion.organizador_principal,
                fecha_subida=reunion.fecha_inicio - timedelta(days=3)
            ),
            DocumentoEmbebido(
                titulo=f'Lista de Participantes - {reunion.titulo}',
                descripcion=f'Lista oficial de participantes de la {reunion.titulo}',
                tipo='ACTA',
                url=f'https://drive.google.com/file/d/participantes_{i+1}/view',
                formato='xlsx',
                tamaño=random.randint(100000, 500000),
                version='1.0',
                subido_por=reunion.organizador_principal,
                fecha_subida=reunion.fecha_inicio - timedelta(days=1)
            )
        ]
        reunion.documentos = documentos_reunion
        
        reunion.save()
    
    # ============================================================================
    # GENERAR ACUERDOS (más completos)
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
            'reunion': reuniones_creadas[4],
            'responsable': 'Dr. Carlos Alberto Ramírez Vargas',
            'fecha_limite': datetime(2025, 12, 31, 23, 59, 59)
        },
        {
            'titulo': 'Implementación de programas de movilidad estudiantil',
            'descripcion': 'Se acuerda implementar programas de movilidad estudiantil entre institutos tecnológicos para fomentar el intercambio académico y cultural.',
            'categoria': 'ACADEMICA',
            'estado': 'COMPLETADO',
            'prioridad': 'MEDIA',
            'reunion': reuniones_creadas[1],
            'responsable': 'Dr. Roberto Carlos Hernández González',
            'fecha_limite': datetime(2024, 12, 31, 23, 59, 59)
        },
        {
            'titulo': 'Desarrollo de plataforma digital unificada',
            'descripcion': 'Se acuerda desarrollar una plataforma digital unificada para la gestión académica y administrativa de todos los institutos tecnológicos del TecNM.',
            'categoria': 'INFRAESTRUCTURA',
            'estado': 'PENDIENTE',
            'prioridad': 'CRITICA',
            'reunion': reuniones_creadas[4],
            'responsable': 'Ing. Roberto Martínez Castro',
            'fecha_limite': datetime(2025, 9, 30, 23, 59, 59)
        },
        {
            'titulo': 'Fortalecimiento de la investigación aplicada',
            'descripcion': 'Se acuerda fortalecer la investigación aplicada en áreas prioritarias como energías renovables, inteligencia artificial, biotecnología y manufactura avanzada.',
            'categoria': 'INVESTIGACION',
            'estado': 'EN_PROCESO',
            'prioridad': 'ALTA',
            'reunion': reuniones_creadas[1],
            'responsable': 'Dr. Alejandro Pérez Gutiérrez',
            'fecha_limite': datetime(2025, 8, 31, 23, 59, 59)
        },
        {
            'titulo': 'Optimización de procesos administrativos',
            'descripcion': 'Se acuerda optimizar los procesos administrativos mediante la implementación de sistemas de gestión integral y automatización de trámites.',
            'categoria': 'ADMINISTRATIVA',
            'estado': 'COMPLETADO',
            'prioridad': 'MEDIA',
            'reunion': reuniones_creadas[3],
            'responsable': 'Lic. Gabriela Martínez López',
            'fecha_limite': datetime(2024, 11, 30, 23, 59, 59)
        },
        {
            'titulo': 'Implementación de programas de capacitación docente',
            'descripcion': 'Se acuerda implementar programas de capacitación docente en nuevas tecnologías y metodologías de enseñanza para mejorar la calidad educativa.',
            'categoria': 'ACADEMICA',
            'estado': 'EN_PROCESO',
            'prioridad': 'ALTA',
            'reunion': reuniones_creadas[0],
            'responsable': 'Dra. Carmen Reyes Navarro',
            'fecha_limite': datetime(2025, 5, 31, 23, 59, 59)
        }
    ]
    
    acuerdos_creados = []
    for i, data in enumerate(acuerdos_data):
        acuerdo = Acuerdo(**data)
        acuerdo.save()
        acuerdos_creados.append(acuerdo)
        print(f"✅ Acuerdo creado: {acuerdo.titulo}")
        
        # Agregar seguimientos embebidos
        from mi_aplication.models import SeguimientoEmbebido
        seguimientos = []
        if acuerdo.estado in ['EN_PROCESO', 'COMPLETADO']:
            # Seguimiento inicial
            seguimientos.append(SeguimientoEmbebido(
                fecha_seguimiento=acuerdo.reunion.fecha_fin + timedelta(days=1),
                estado_anterior='PENDIENTE',
                estado_nuevo='EN_PROCESO',
                porcentaje_avance=10,
                observaciones='Acuerdo aprobado en reunión. Iniciando proceso de implementación.',
                responsable=acuerdo.responsable
            ))
            
            # Seguimientos intermedios
            if acuerdo.estado == 'EN_PROCESO':
                seguimientos.append(SeguimientoEmbebido(
                    fecha_seguimiento=datetime.now() - timedelta(days=random.randint(10, 30)),
                    estado_anterior='EN_PROCESO',
                    estado_nuevo='EN_PROCESO',
                    porcentaje_avance=random.randint(25, 75),
                    observaciones=random.choice([
                        'Proceso de implementación en curso. Avances significativos realizados.',
                        'Documentación y planificación completadas. Iniciando fase de ejecución.',
                        'Coordinación con equipos de trabajo establecida. Progreso satisfactorio.',
                        'Recursos asignados y cronograma establecido. Proyecto en marcha.'
                    ]),
                    responsable=acuerdo.responsable
                ))
            elif acuerdo.estado == 'COMPLETADO':
                seguimientos.append(SeguimientoEmbebido(
                    fecha_seguimiento=datetime.now() - timedelta(days=random.randint(5, 15)),
                    estado_anterior='EN_PROCESO',
                    estado_nuevo='COMPLETADO',
                    porcentaje_avance=100,
                    observaciones='Acuerdo implementado exitosamente. Objetivos cumplidos al 100%.',
                    responsable=acuerdo.responsable
                ))
        
        acuerdo.seguimientos = seguimientos
        
        # Agregar documentos embebidos
        documentos_acuerdo = [
            DocumentoEmbebido(
                titulo=f'Propuesta de {acuerdo.titulo}',
                descripcion=f'Propuesta detallada para la implementación del acuerdo: {acuerdo.titulo}',
                tipo='PRESENTACION',
                url=f'https://drive.google.com/file/d/propuesta_acuerdo_{i+1}/view',
                formato='pptx',
                tamaño=random.randint(2000000, 8000000),
                version='1.0',
                subido_por=acuerdo.responsable,
                fecha_subida=acuerdo.reunion.fecha_fin + timedelta(days=2)
            ),
            DocumentoEmbebido(
                titulo=f'Plan de Implementación - {acuerdo.titulo}',
                descripcion=f'Plan detallado de implementación para el acuerdo: {acuerdo.titulo}',
                tipo='MEMORANDUM',
                url=f'https://drive.google.com/file/d/plan_acuerdo_{i+1}/view',
                formato='pdf',
                tamaño=random.randint(1000000, 3000000),
                version='1.0',
                subido_por=acuerdo.responsable,
                fecha_subida=acuerdo.reunion.fecha_fin + timedelta(days=5)
            )
        ]
        
        if acuerdo.estado in ['EN_PROCESO', 'COMPLETADO']:
            documentos_acuerdo.append(DocumentoEmbebido(
                titulo=f'Reporte de Avance - {acuerdo.titulo}',
                descripcion=f'Reporte de avance del acuerdo: {acuerdo.titulo}',
                tipo='CIRCULAR',
                url=f'https://drive.google.com/file/d/avance_acuerdo_{i+1}/view',
                formato='pdf',
                tamaño=random.randint(500000, 1500000),
                version='1.0',
                subido_por=acuerdo.responsable,
                fecha_subida=datetime.now() - timedelta(days=random.randint(1, 10))
            ))
        
        acuerdo.documentos = documentos_acuerdo
        acuerdo.save()
    
    # ============================================================================
    # GENERAR DOCUMENTOS INDEPENDIENTES
    # ============================================================================
    print("\n📄 Generando documentos independientes...")
    
    documentos_data = [
        {
            'titulo': 'Manual de Procedimientos del TecNM',
            'descripcion': 'Manual actualizado de procedimientos administrativos y académicos del TecNM',
            'tipo': 'CIRCULAR',
            'url': 'https://drive.google.com/file/d/manual_procedimientos_2024/view',
            'formato': 'pdf',
            'tamaño': 5000000,
            'version': '2024.1',
            'subido_por': 'Dr. Juan Carlos García Rodríguez',
            'fecha_subida': datetime(2024, 10, 15, 10, 0)
        },
        {
            'titulo': 'Estadísticas de Egresados 2024',
            'descripcion': 'Reporte estadístico de egresados de todos los institutos tecnológicos del TecNM',
            'tipo': 'ACTA',
            'url': 'https://drive.google.com/file/d/estadisticas_egresados_2024/view',
            'formato': 'xlsx',
            'tamaño': 2500000,
            'version': '1.0',
            'subido_por': 'Lic. Gabriela Martínez López',
            'fecha_subida': datetime(2024, 11, 20, 14, 30)
        },
        {
            'titulo': 'Guía de Mejores Prácticas en Investigación',
            'descripcion': 'Guía actualizada de mejores prácticas en investigación para docentes del TecNM',
            'tipo': 'MEMORANDUM',
            'url': 'https://drive.google.com/file/d/guia_investigacion_2024/view',
            'formato': 'pdf',
            'tamaño': 3500000,
            'version': '2024.2',
            'subido_por': 'Dr. Alejandro Pérez Gutiérrez',
            'fecha_subida': datetime(2024, 9, 10, 9, 15)
        },
        {
            'titulo': 'Protocolo de Seguridad Informática',
            'descripcion': 'Protocolo actualizado de seguridad informática para todos los institutos tecnológicos',
            'tipo': 'CIRCULAR',
            'url': 'https://drive.google.com/file/d/protocolo_seguridad_2024/view',
            'formato': 'pdf',
            'tamaño': 4000000,
            'version': '2024.1',
            'subido_por': 'Ing. Roberto Martínez Castro',
            'fecha_subida': datetime(2024, 8, 25, 16, 45)
        },
        {
            'titulo': 'Catálogo de Programas Educativos 2024',
            'descripcion': 'Catálogo actualizado de programas educativos ofertados por el TecNM',
            'tipo': 'PRESENTACION',
            'url': 'https://drive.google.com/file/d/catalogo_programas_2024/view',
            'formato': 'pptx',
            'tamaño': 8000000,
            'version': '2024.1',
            'subido_por': 'Dra. María Elena López Martínez',
            'fecha_subida': datetime(2024, 7, 15, 11, 20)
        }
    ]
    
    for data in documentos_data:
        documento = Documento(**data)
        documento.save()
        print(f"✅ Documento creado: {documento.titulo}")
    
    print(f"\n🎉 ¡Datos fake mejorados generados exitosamente!")
    print(f"📊 Resumen:")
    print(f"   • {len(participantes_creados)} participantes")
    print(f"   • {len(reuniones_creadas)} reuniones nacionales")
    print(f"   • {len(acuerdos_creados)} acuerdos")
    print(f"   • {len(documentos_data)} documentos independientes")
    print(f"   • Cada reunión tiene participantes, agenda y documentos embebidos")
    print(f"   • Cada acuerdo tiene seguimientos y documentos embebidos")

if __name__ == '__main__':
    try:
        generar_datos_fake_mejorados()
    except Exception as e:
        print(f"❌ Error al generar datos: {e}")
        import traceback
        traceback.print_exc()
