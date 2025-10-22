#!/usr/bin/env python
"""
Script para migrar participantes de campos antiguos a nuevos
- instituto -> plantel_tecnm
- departamento -> area_departamento
- jefe_departamento -> jefe_inmediato
- correo_jefe_departamento -> correo_jefe_inmediato
- Agregar: RFC, CURP, sexo, edad, puesto, director, correo_direccion
"""

import os
import sys
import django
import random
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from pymongo import MongoClient
from django.conf import settings
from mi_aplication.constants import (
    PLANTELES_TECNM, AREAS_DEPARTAMENTO, SEXOS,
    CATEGORIAS_FORMATIVAS, CURSOS_ESPECIFICOS
)

# Datos fake para generar
JEFES_FAKE = [
    "Dr. Carlos Mendoza López",
    "Dra. María Elena García",
    "Ing. Roberto Sánchez Ruiz",
    "Lic. Laura Patricia Torres",
    "M.C. Fernando Jiménez Vega",
    "Dr. Miguel Ángel Herrera",
    "Dra. Ana Luisa Rodríguez",
    "Ing. José Luis Martínez"
]

DIRECTORES_FAKE = [
    "Dr. Juan Alberto Ramírez",
    "Dra. Patricia Gómez Castro",
    "Ing. Ricardo Hernández Silva",
    "Dr. Eduardo Torres Méndez",
    "Dra. Claudia Morales Vega"
]

PUESTOS_FAKE = [
    "Profesor de Tiempo Completo",
    "Profesor de Asignatura",
    "Investigador",
    "Jefe de Departamento",
    "Coordinador Académico"
]

def generar_rfc_fake(nombre, apellido_paterno, apellido_materno=None):
    """Genera un RFC fake pero con formato válido"""
    # Tomar primeras 2 letras del apellido paterno
    ap = apellido_paterno[:2].upper() if apellido_paterno else "XX"
    # Primera letra del apellido materno
    am = apellido_materno[0].upper() if apellido_materno else "X"
    # Primera letra del nombre
    n = nombre[0].upper() if nombre else "X"
    # Fecha aleatoria (año entre 1960-1990)
    año = random.randint(60, 90)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    # Homoclave aleatoria
    homoclave = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))
    
    return f"{ap}{am}{n}{año:02d}{mes:02d}{dia:02d}{homoclave}"

def generar_curp_fake(nombre, apellido_paterno, apellido_materno, sexo):
    """Genera una CURP fake pero con formato válido"""
    # Primeras 4 letras igual que RFC
    ap = apellido_paterno[:2].upper() if apellido_paterno else "XX"
    am = apellido_materno[0].upper() if apellido_materno else "X"
    n = nombre[0].upper() if nombre else "X"
    
    # Fecha (año entre 1960-1990)
    año = random.randint(60, 90)
    mes = random.randint(1, 12)
    dia = random.randint(1, 28)
    
    # Sexo
    sexo_letra = sexo if sexo in ['M', 'F'] else random.choice(['M', 'F'])
    
    # Estado (aleatorio)
    estados = ['AS', 'BC', 'BS', 'CC', 'CH', 'CL', 'CM', 'CS', 'DF', 'DG', 
               'GT', 'GR', 'HG', 'JC', 'MC', 'MN', 'MS', 'NE', 'NL', 'NT']
    estado = random.choice(estados)
    
    # Consonantes internas y dígito verificador
    consonantes = ''.join(random.choices('BCDFGHJKLMNPQRSTVWXYZ', k=3))
    digito = random.choice('0123456789')
    
    return f"{ap}{am}{n}{año:02d}{mes:02d}{dia:02d}{sexo_letra}{estado}{consonantes}{digito}"

def migrar_participantes():
    """Migra todos los participantes existentes"""
    print("=" * 80)
    print("MIGRANDO PARTICIPANTES - ACTUALIZANDO CAMPOS")
    print("=" * 80)
    
    # Conectar a MongoDB directamente usando MONGODB_SETTINGS
    mongodb_config = settings.MONGODB_SETTINGS
    client = MongoClient(
        host=mongodb_config.get('host', '127.0.0.1'),
        port=mongodb_config.get('port', 27017),
        username=mongodb_config.get('username'),
        password=mongodb_config.get('password'),
        authSource=mongodb_config.get('authentication_source', 'admin'),
        authMechanism=mongodb_config.get('authentication_mechanism', 'SCRAM-SHA-1')
    )
    db = client[mongodb_config['db']]
    collection = db['participantes']
    
    # Obtener todos los documentos
    documentos = list(collection.find())
    total = len(documentos)
    
    print(f"\nTotal de participantes a procesar: {total}\n")
    
    actualizados = 0
    errores = 0
    
    planteles_codigos = [codigo for codigo, _ in PLANTELES_TECNM]
    areas_codigos = [codigo for codigo, _ in AREAS_DEPARTAMENTO]
    sexos_valores = [codigo for codigo, _ in SEXOS]
    
    for i, doc in enumerate(documentos, 1):
        try:
            nombre = doc.get('nombre', 'Desconocido')
            apellido_paterno = doc.get('apellido_paterno', '')
            apellido_materno = doc.get('apellido_materno', '')
            
            print(f"\n[{i}/{total}] Procesando: {nombre} {apellido_paterno}")
            
            # Diccionarios para actualización
            set_updates = {}
            unset_fields = {}
            
            # ==== MIGRACIÓN DE CAMPOS ANTIGUOS ====
            
            # 1. Migrar instituto -> plantel_tecnm
            if 'instituto' in doc:
                instituto_valor = doc['instituto']
                if not doc.get('plantel_tecnm'):
                    # Intentar encontrar coincidencia
                    plantel_encontrado = None
                    if instituto_valor:
                        instituto_lower = str(instituto_valor).lower()
                        for codigo, nombre_plantel in PLANTELES_TECNM:
                            if (codigo.lower() in instituto_lower or 
                                instituto_lower in nombre_plantel.lower()):
                                plantel_encontrado = codigo
                                break
                    
                    if not plantel_encontrado:
                        plantel_encontrado = random.choice(planteles_codigos)
                    
                    set_updates['plantel_tecnm'] = plantel_encontrado
                    print(f"  + plantel_tecnm = {plantel_encontrado}")
                
                # Marcar para eliminar
                unset_fields['instituto'] = ''
                print(f"  - eliminado campo 'instituto'")
            elif not doc.get('plantel_tecnm'):
                # No tiene ninguno, asignar aleatorio
                plantel_aleatorio = random.choice(planteles_codigos)
                set_updates['plantel_tecnm'] = plantel_aleatorio
                print(f"  + plantel_tecnm = {plantel_aleatorio}")
            
            # 2. Migrar departamento -> area_departamento
            if 'departamento' in doc:
                dept_valor = doc['departamento']
                if not doc.get('area_departamento'):
                    # Intentar encontrar coincidencia
                    area_encontrada = None
                    if dept_valor:
                        dept_lower = str(dept_valor).lower()
                        for codigo, nombre_area in AREAS_DEPARTAMENTO:
                            if (codigo.lower() in dept_lower or 
                                dept_lower in nombre_area.lower()):
                                area_encontrada = codigo
                                break
                    
                    if not area_encontrada:
                        area_encontrada = random.choice(areas_codigos)
                    
                    set_updates['area_departamento'] = area_encontrada
                    print(f"  + area_departamento = {area_encontrada}")
                
                # Marcar para eliminar
                unset_fields['departamento'] = ''
                print(f"  - eliminado campo 'departamento'")
            elif not doc.get('area_departamento'):
                # No tiene ninguno, asignar aleatorio
                area_aleatoria = random.choice(areas_codigos)
                set_updates['area_departamento'] = area_aleatoria
                print(f"  + area_departamento = {area_aleatoria}")
            
            # 3. Migrar jefe_departamento -> jefe_inmediato
            if 'jefe_departamento' in doc and doc['jefe_departamento']:
                if not doc.get('jefe_inmediato'):
                    set_updates['jefe_inmediato'] = doc['jefe_departamento']
                    print(f"  + jefe_inmediato = {doc['jefe_departamento']}")
                unset_fields['jefe_departamento'] = ''
            elif not doc.get('jefe_inmediato'):
                jefe_fake = random.choice(JEFES_FAKE)
                set_updates['jefe_inmediato'] = jefe_fake
                print(f"  + jefe_inmediato = {jefe_fake}")
            
            # 4. Migrar correo_jefe_departamento -> correo_jefe_inmediato
            if 'correo_jefe_departamento' in doc and doc['correo_jefe_departamento']:
                if not doc.get('correo_jefe_inmediato'):
                    set_updates['correo_jefe_inmediato'] = doc['correo_jefe_departamento']
                    print(f"  + correo_jefe_inmediato = {doc['correo_jefe_departamento']}")
                unset_fields['correo_jefe_departamento'] = ''
            elif not doc.get('correo_jefe_inmediato'):
                # Generar correo fake basado en el jefe
                jefe = set_updates.get('jefe_inmediato', doc.get('jefe_inmediato', ''))
                if jefe:
                    jefe_parts = jefe.split()
                    if len(jefe_parts) >= 2:
                        correo_fake = f"{jefe_parts[-1].lower()}.{jefe_parts[0].lower()}@tecnm.mx"
                    else:
                        correo_fake = f"jefe.{random.randint(1,999)}@tecnm.mx"
                    set_updates['correo_jefe_inmediato'] = correo_fake
                    print(f"  + correo_jefe_inmediato = {correo_fake}")
            
            # ==== AGREGAR NUEVOS CAMPOS FALTANTES ====
            
            # 5. RFC
            if not doc.get('rfc'):
                rfc_fake = generar_rfc_fake(nombre, apellido_paterno, apellido_materno)
                set_updates['rfc'] = rfc_fake
                print(f"  + rfc = {rfc_fake}")
            
            # 6. Sexo (necesario para CURP)
            sexo_actual = doc.get('sexo')
            if not sexo_actual:
                sexo_actual = random.choice(sexos_valores)
                set_updates['sexo'] = sexo_actual
                print(f"  + sexo = {sexo_actual}")
            
            # 7. CURP
            if not doc.get('curp'):
                curp_fake = generar_curp_fake(nombre, apellido_paterno, apellido_materno, 
                                             set_updates.get('sexo', sexo_actual))
                set_updates['curp'] = curp_fake
                print(f"  + curp = {curp_fake}")
            
            # 8. Edad
            if not doc.get('edad'):
                edad_fake = random.randint(25, 65)
                set_updates['edad'] = edad_fake
                print(f"  + edad = {edad_fake}")
            
            # 9. Puesto
            if not doc.get('puesto'):
                puesto_fake = random.choice(PUESTOS_FAKE)
                set_updates['puesto'] = puesto_fake
                print(f"  + puesto = {puesto_fake}")
            
            # 10. Director
            if not doc.get('director'):
                director_fake = random.choice(DIRECTORES_FAKE)
                set_updates['director'] = director_fake
                print(f"  + director = {director_fake}")
            
            # 11. Correo dirección
            if not doc.get('correo_direccion'):
                plantel = set_updates.get('plantel_tecnm', doc.get('plantel_tecnm', 'tecnm'))
                correo_dir_fake = f"direccion.{plantel.lower()}@tecnm.mx"
                set_updates['correo_direccion'] = correo_dir_fake
                print(f"  + correo_direccion = {correo_dir_fake}")
            
            # ==== EJECUTAR ACTUALIZACIÓN ====
            if set_updates or unset_fields:
                update_query = {}
                if set_updates:
                    update_query['$set'] = set_updates
                if unset_fields:
                    update_query['$unset'] = unset_fields
                
                result = collection.update_one(
                    {'_id': doc['_id']},
                    update_query
                )
                
                if result.modified_count > 0:
                    actualizados += 1
                    print(f"  ✓ Actualizado correctamente")
                else:
                    print(f"  • Sin cambios necesarios")
            else:
                print(f"  • Todos los campos ya están actualizados")
                
        except Exception as e:
            errores += 1
            print(f"  ✗ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"Total procesados: {total}")
    print(f"Actualizados: {actualizados}")
    print(f"Errores: {errores}")
    print(f"Sin cambios: {total - actualizados - errores}")
    print("=" * 80)
    
    client.close()

if __name__ == '__main__':
    try:
        migrar_participantes()
        print("\n✓ Migración completada exitosamente")
    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
