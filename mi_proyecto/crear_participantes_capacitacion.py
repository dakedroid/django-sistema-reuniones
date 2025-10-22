"""
Script para crear participantes de ejemplo con categorías formativas y cursos específicos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import Participante
from mi_aplication.constants import CATEGORIAS_FORMATIVAS, CURSOS_ESPECIFICOS

# Datos de participantes de ejemplo usando las categorías de CATEGORIAS_FORMATIVAS
participantes_ejemplo = [
    # Docente TecNM
    {
        'nombre': 'Juan',
        'apellido_paterno': 'García',
        'apellido_materno': 'López',
        'email': 'juan.garcia@tecnm.mx',
        'telefono': '+52 444 123 4567',
        'instituto': 'Instituto Tecnológico de San Luis Potosí',
        'departamento': 'Docencia',
        'tipo_participante': 'DOCENTE_TECNM',
        'categoria_formativa': 'DOCENTE_TECNM',
        'cursos_especificos': ['PEDAGOGIA_DIGITAL', 'METODOLOGIAS_ACTIVAS'],
        'confirmado': True,
    },
    {
        'nombre': 'María',
        'apellido_paterno': 'Hernández',
        'apellido_materno': 'Ramírez',
        'email': 'maria.hernandez@tecnm.mx',
        'telefono': '+52 444 234 5678',
        'instituto': 'Instituto Tecnológico de Celaya',
        'departamento': 'Docencia',
        'tipo_participante': 'DOCENTE_TECNM',
        'categoria_formativa': 'DOCENTE_TECNM',
        'cursos_especificos': ['EVALUACION_EDUCATIVA', 'DISEÑO_CURRICULAR'],
        'confirmado': True,
    },
    {
        'nombre': 'Carlos',
        'apellido_paterno': 'Martínez',
        'apellido_materno': 'Sánchez',
        'email': 'carlos.martinez@tecnm.mx',
        'telefono': '+52 444 345 6789',
        'instituto': 'Instituto Tecnológico de Tijuana',
        'departamento': 'Docencia',
        'tipo_participante': 'DOCENTE_TECNM',
        'categoria_formativa': 'DOCENTE_TECNM',
        'cursos_especificos': ['COMPETENCIAS_DIGITALES', 'EDUCACION_VIRTUAL'],
        'confirmado': True,
    },
    
    # Matemáticas y Ciencias Básicas
    {
        'nombre': 'Ana',
        'apellido_paterno': 'Rodríguez',
        'apellido_materno': 'González',
        'email': 'ana.rodriguez@tecnm.mx',
        'telefono': '+52 444 456 7890',
        'instituto': 'Instituto Tecnológico de Monterrey',
        'departamento': 'Ciencias Básicas',
        'tipo_participante': 'MATEMATICAS_CIENCIAS',
        'categoria_formativa': 'MATEMATICAS_CIENCIAS',
        'cursos_especificos': ['ESTADISTICA_AVANZADA', 'METODOLOGIA_INVESTIGACION'],
        'confirmado': True,
    },
    {
        'nombre': 'Luis',
        'apellido_paterno': 'Pérez',
        'apellido_materno': 'Torres',
        'email': 'luis.perez@tecnm.mx',
        'telefono': '+52 444 567 8901',
        'instituto': 'Instituto Tecnológico de Aguascalientes',
        'departamento': 'Matemáticas',
        'tipo_participante': 'MATEMATICAS_CIENCIAS',
        'categoria_formativa': 'MATEMATICAS_CIENCIAS',
        'cursos_especificos': ['ESTADISTICA_AVANZADA'],
        'confirmado': True,
    },
    {
        'nombre': 'Laura',
        'apellido_paterno': 'Gómez',
        'apellido_materno': 'Díaz',
        'email': 'laura.gomez@tecnm.mx',
        'telefono': '+52 444 678 9012',
        'instituto': 'Instituto Tecnológico de Querétaro',
        'departamento': 'Física',
        'tipo_participante': 'MATEMATICAS_CIENCIAS',
        'categoria_formativa': 'MATEMATICAS_CIENCIAS',
        'cursos_especificos': ['METODOLOGIA_INVESTIGACION', 'REDACCION_CIENTIFICA'],
        'confirmado': True,
    },
    
    # Tecnologías - Ciencia de Datos
    {
        'nombre': 'Roberto',
        'apellido_paterno': 'Flores',
        'apellido_materno': 'Ruiz',
        'email': 'roberto.flores@tecnm.mx',
        'telefono': '+52 444 789 0123',
        'instituto': 'Instituto Tecnológico de Toluca',
        'departamento': 'Sistemas y Computación',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['CIENCIA_DATOS', 'BIG_DATA'],
        'confirmado': True,
    },
    {
        'nombre': 'Patricia',
        'apellido_paterno': 'Morales',
        'apellido_materno': 'Castro',
        'email': 'patricia.morales@tecnm.mx',
        'telefono': '+52 444 890 1234',
        'instituto': 'Instituto Tecnológico de Puebla',
        'departamento': 'Sistemas y Computación',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['CIENCIA_DATOS', 'MACHINE_LEARNING'],
        'confirmado': True,
    },
    {
        'nombre': 'Fernando',
        'apellido_paterno': 'Ramírez',
        'apellido_materno': 'Ortiz',
        'email': 'fernando.ramirez@tecnm.mx',
        'telefono': '+52 444 901 2345',
        'instituto': 'Instituto Tecnológico de Mérida',
        'departamento': 'Ingeniería en Datos',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['CIENCIA_DATOS', 'ESTADISTICA_AVANZADA'],
        'confirmado': True,
    },
    
    # Tecnologías - Inteligencia Artificial
    {
        'nombre': 'Sandra',
        'apellido_paterno': 'Vargas',
        'apellido_materno': 'Mendoza',
        'email': 'sandra.vargas@tecnm.mx',
        'telefono': '+52 444 012 3456',
        'instituto': 'Instituto Tecnológico de Guadalajara',
        'departamento': 'Sistemas y Computación',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['INTELIGENCIA_ARTIFICIAL', 'MACHINE_LEARNING'],
        'confirmado': True,
    },
    {
        'nombre': 'Miguel',
        'apellido_paterno': 'Jiménez',
        'apellido_materno': 'Vega',
        'email': 'miguel.jimenez@tecnm.mx',
        'telefono': '+52 444 123 4560',
        'instituto': 'Instituto Tecnológico de León',
        'departamento': 'Inteligencia Artificial',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['INTELIGENCIA_ARTIFICIAL', 'DEEP_LEARNING'],
        'confirmado': True,
    },
    {
        'nombre': 'Diana',
        'apellido_paterno': 'Cruz',
        'apellido_materno': 'Reyes',
        'email': 'diana.cruz@tecnm.mx',
        'telefono': '+52 444 234 5671',
        'instituto': 'Instituto Tecnológico de Chihuahua',
        'departamento': 'Computación Avanzada',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['INTELIGENCIA_ARTIFICIAL', 'VISION_COMPUTACIONAL'],
        'confirmado': True,
    },
    
    # Tecnologías - Desarrollo de Apps
    {
        'nombre': 'Jorge',
        'apellido_paterno': 'Medina',
        'apellido_materno': 'Silva',
        'email': 'jorge.medina@tecnm.mx',
        'telefono': '+52 444 345 6782',
        'instituto': 'Instituto Tecnológico de Veracruz',
        'departamento': 'Desarrollo de Software',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['DESARROLLO_MOVIL', 'DESARROLLO_WEB'],
        'confirmado': True,
    },
    {
        'nombre': 'Alejandra',
        'apellido_paterno': 'Romero',
        'apellido_materno': 'Guzmán',
        'email': 'alejandra.romero@tecnm.mx',
        'telefono': '+52 444 456 7893',
        'instituto': 'Instituto Tecnológico de Durango',
        'departamento': 'Ingeniería de Software',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['DESARROLLO_MOVIL', 'CLOUD_COMPUTING'],
        'confirmado': True,
    },
    {
        'nombre': 'Ricardo',
        'apellido_paterno': 'Ortega',
        'apellido_materno': 'Navarro',
        'email': 'ricardo.ortega@tecnm.mx',
        'telefono': '+52 444 567 8904',
        'instituto': 'Instituto Tecnológico de Oaxaca',
        'departamento': 'Desarrollo de Apps',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['DESARROLLO_MOVIL', 'UX_UI_DESIGN'],
        'confirmado': True,
    },
    
    # Más participantes para Tecnologías con múltiples cursos
    {
        'nombre': 'Elena',
        'apellido_paterno': 'Campos',
        'apellido_materno': 'Luna',
        'email': 'elena.campos@tecnm.mx',
        'telefono': '+52 444 678 9015',
        'instituto': 'Instituto Tecnológico de Zacatecas',
        'departamento': 'Tecnologías Emergentes',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['CIENCIA_DATOS', 'INTELIGENCIA_ARTIFICIAL', 'DESARROLLO_MOVIL'],
        'confirmado': True,
    },
    {
        'nombre': 'Daniel',
        'apellido_paterno': 'Núñez',
        'apellido_materno': 'Ponce',
        'email': 'daniel.nunez@tecnm.mx',
        'telefono': '+52 444 789 0126',
        'instituto': 'Instituto Tecnológico de Culiacán',
        'departamento': 'Innovación Tecnológica',
        'tipo_participante': 'DOCENTE',
        'categoria_formativa': 'TECNOLOGIAS',
        'cursos_especificos': ['CLOUD_COMPUTING', 'CIBERSEGURIDAD', 'IOT'],
        'confirmado': True,
    },
]

def crear_participantes():
    """Crea participantes de ejemplo en la base de datos"""
    print("=" * 60)
    print("CREANDO PARTICIPANTES DE EJEMPLO CON CAPACITACIONES")
    print("=" * 60)
    
    participantes_creados = 0
    participantes_actualizados = 0
    errores = 0
    
    for datos in participantes_ejemplo:
        try:
            # Verificar si el participante ya existe por email
            participante_existente = Participante.objects.filter(email=datos['email']).first()
            
            if participante_existente:
                # Actualizar participante existente
                for key, value in datos.items():
                    setattr(participante_existente, key, value)
                participante_existente.save()
                participantes_actualizados += 1
                print(f"✓ Actualizado: {datos['nombre']} {datos['apellido_paterno']} - {datos['categoria_formativa']}")
            else:
                # Crear nuevo participante
                participante = Participante(**datos)
                participante.save()
                participantes_creados += 1
                print(f"✓ Creado: {datos['nombre']} {datos['apellido_paterno']} - {datos['categoria_formativa']}")
                
        except Exception as e:
            errores += 1
            print(f"✗ Error con {datos['nombre']} {datos['apellido_paterno']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print(f"Participantes creados: {participantes_creados}")
    print(f"Participantes actualizados: {participantes_actualizados}")
    print(f"Errores: {errores}")
    print(f"Total procesados: {len(participantes_ejemplo)}")
    
    # Mostrar estadísticas por categoría
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS POR CATEGORÍA FORMATIVA")
    print("=" * 60)
    
    categorias = {}
    for datos in participantes_ejemplo:
        cat = datos['categoria_formativa']
        if cat not in categorias:
            categorias[cat] = {'total': 0, 'cursos': set()}
        categorias[cat]['total'] += 1
        categorias[cat]['cursos'].update(datos['cursos_especificos'])
    
    dict_categorias = dict(CATEGORIAS_FORMATIVAS)
    for codigo, stats in categorias.items():
        nombre = dict_categorias.get(codigo, codigo)
        print(f"\n{nombre}:")
        print(f"  Total participantes: {stats['total']}")
        print(f"  Cursos distintos: {len(stats['cursos'])}")
        print(f"  Cursos: {', '.join(stats['cursos'])}")
    
    print("\n" + "=" * 60)
    print("¡PROCESO COMPLETADO!")
    print("=" * 60)

if __name__ == '__main__':
    crear_participantes()
