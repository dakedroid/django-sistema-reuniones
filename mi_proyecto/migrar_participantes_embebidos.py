#!/usr/bin/env python
"""
Script para migrar participantes EMBEBIDOS en reuniones
- instituto -> plantel_tecnm
- departamento -> area_departamento
"""

import os
import sys
import django
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from pymongo import MongoClient
from django.conf import settings
from mi_aplication.constants import PLANTELES_TECNM, AREAS_DEPARTAMENTO

def migrar_participantes_embebidos():
    """Migra los participantes embebidos en las reuniones"""
    print("=" * 80)
    print("MIGRANDO PARTICIPANTES EMBEBIDOS EN REUNIONES")
    print("=" * 80)
    
    # Conectar a MongoDB directamente
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
    collection = db['reunion_nacional']
    
    # Obtener todas las reuniones que tienen participantes
    reuniones = list(collection.find({'participantes': {'$exists': True, '$ne': []}}))
    total = len(reuniones)
    
    print(f"\nTotal de reuniones con participantes a procesar: {total}\n")
    
    actualizados = 0
    errores = 0
    
    planteles_codigos = [codigo for codigo, _ in PLANTELES_TECNM]
    areas_codigos = [codigo for codigo, _ in AREAS_DEPARTAMENTO]
    
    for i, reunion in enumerate(reuniones, 1):
        try:
            titulo = reunion.get('titulo', 'Sin título')
            participantes = reunion.get('participantes', [])
            
            if not participantes:
                continue
            
            print(f"\n[{i}/{total}] Reunión: {titulo}")
            print(f"  Participantes a revisar: {len(participantes)}")
            
            participantes_actualizados = []
            cambios_realizados = False
            
            for j, participante in enumerate(participantes, 1):
                cambios_participante = {}
                
                # Migrar instituto -> plantel_tecnm
                if 'instituto' in participante:
                    instituto_valor = participante.get('instituto')
                    
                    # Si no tiene plantel_tecnm, intentar mapear o asignar aleatorio
                    if 'plantel_tecnm' not in participante or not participante.get('plantel_tecnm'):
                        plantel_encontrado = None
                        
                        if instituto_valor:
                            instituto_lower = str(instituto_valor).lower()
                            for codigo, nombre in PLANTELES_TECNM:
                                if (codigo.lower() in instituto_lower or 
                                    instituto_lower in nombre.lower()):
                                    plantel_encontrado = codigo
                                    break
                        
                        if not plantel_encontrado:
                            plantel_encontrado = random.choice(planteles_codigos)
                        
                        cambios_participante['plantel_tecnm'] = plantel_encontrado
                        print(f"    Participante {j}: plantel_tecnm = {plantel_encontrado}")
                    else:
                        # Ya tiene plantel_tecnm, conservarlo
                        cambios_participante['plantel_tecnm'] = participante['plantel_tecnm']
                    
                    # Remover campo antiguo
                    cambios_realizados = True
                elif 'plantel_tecnm' in participante:
                    # Ya tiene el campo correcto
                    cambios_participante['plantel_tecnm'] = participante['plantel_tecnm']
                else:
                    # No tiene ninguno, asignar aleatorio
                    plantel_aleatorio = random.choice(planteles_codigos)
                    cambios_participante['plantel_tecnm'] = plantel_aleatorio
                    cambios_realizados = True
                    print(f"    Participante {j}: plantel_tecnm = {plantel_aleatorio} (nuevo)")
                
                # Migrar departamento -> area_departamento
                if 'departamento' in participante:
                    dept_valor = participante.get('departamento')
                    
                    if 'area_departamento' not in participante or not participante.get('area_departamento'):
                        area_encontrada = None
                        
                        if dept_valor:
                            dept_lower = str(dept_valor).lower()
                            for codigo, nombre in AREAS_DEPARTAMENTO:
                                if (codigo.lower() in dept_lower or 
                                    dept_lower in nombre.lower()):
                                    area_encontrada = codigo
                                    break
                        
                        if not area_encontrada:
                            area_encontrada = random.choice(areas_codigos)
                        
                        cambios_participante['area_departamento'] = area_encontrada
                        print(f"    Participante {j}: area_departamento = {area_encontrada}")
                    else:
                        cambios_participante['area_departamento'] = participante['area_departamento']
                    
                    cambios_realizados = True
                elif 'area_departamento' in participante:
                    cambios_participante['area_departamento'] = participante['area_departamento']
                else:
                    area_aleatoria = random.choice(areas_codigos)
                    cambios_participante['area_departamento'] = area_aleatoria
                    cambios_realizados = True
                    print(f"    Participante {j}: area_departamento = {area_aleatoria} (nuevo)")
                
                # Copiar el resto de los campos (excepto instituto y departamento)
                participante_nuevo = {}
                for key, value in participante.items():
                    if key not in ['instituto', 'departamento']:
                        participante_nuevo[key] = value
                
                # Agregar los nuevos campos
                participante_nuevo.update(cambios_participante)
                
                participantes_actualizados.append(participante_nuevo)
            
            # Actualizar la reunión si hubo cambios
            if cambios_realizados:
                result = collection.update_one(
                    {'_id': reunion['_id']},
                    {'$set': {'participantes': participantes_actualizados}}
                )
                
                if result.modified_count > 0:
                    actualizados += 1
                    print(f"  ✓ Reunión actualizada correctamente")
                else:
                    print(f"  • Sin cambios necesarios")
            else:
                # Aunque no hubo cambios en campos, actualizar para asegurar consistencia
                collection.update_one(
                    {'_id': reunion['_id']},
                    {'$set': {'participantes': participantes_actualizados}}
                )
                print(f"  • Participantes ya actualizados")
                
        except Exception as e:
            errores += 1
            print(f"  ✗ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"Total reuniones procesadas: {total}")
    print(f"Actualizadas: {actualizados}")
    print(f"Errores: {errores}")
    print(f"Sin cambios: {total - actualizados - errores}")
    print("=" * 80)
    
    client.close()

if __name__ == '__main__':
    try:
        migrar_participantes_embebidos()
        print("\n✓ Migración de participantes embebidos completada exitosamente")
    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
