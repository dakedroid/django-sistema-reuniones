#!/usr/bin/env python
"""
Script para migrar ParticipantesEmbebidos en las reuniones
Eliminar campos antiguos: instituto, departamento
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from pymongo import MongoClient
from django.conf import settings

def migrar_participantes_embebidos():
    """Migra participantes embebidos en las reuniones"""
    print("=" * 80)
    print("MIGRANDO PARTICIPANTES EMBEBIDOS EN REUNIONES")
    print("=" * 80)
    
    # Conectar a MongoDB
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
    
    # Obtener todas las reuniones
    reuniones = list(collection.find())
    total = len(reuniones)
    
    print(f"\nTotal de reuniones a procesar: {total}\n")
    
    actualizadas = 0
    errores = 0
    
    for i, reunion in enumerate(reuniones, 1):
        try:
            titulo = reunion.get('titulo', 'Sin título')
            print(f"\n[{i}/{total}] Procesando: {titulo}")
            
            participantes = reunion.get('participantes', {})
            if not participantes:
                print("  • Sin participantes")
                continue
            
            participantes_modificados = False
            participantes_actualizados = {}
            
            # Procesar cada participante embebido
            for part_id, part_data in participantes.items():
                cambios = False
                
                # Eliminar campos antiguos si existen
                if 'instituto' in part_data:
                    del part_data['instituto']
                    cambios = True
                    print(f"  - Eliminado 'instituto' de participante {part_id}")
                
                if 'departamento' in part_data:
                    del part_data['departamento']
                    cambios = True
                    print(f"  - Eliminado 'departamento' de participante {part_id}")
                
                participantes_actualizados[part_id] = part_data
                if cambios:
                    participantes_modificados = True
            
            # Actualizar la reunión si hubo cambios
            if participantes_modificados:
                result = collection.update_one(
                    {'_id': reunion['_id']},
                    {'$set': {'participantes': participantes_actualizados}}
                )
                
                if result.modified_count > 0:
                    actualizadas += 1
                    print(f"  ✓ Reunión actualizada")
            else:
                print(f"  • Sin cambios necesarios")
                
        except Exception as e:
            errores += 1
            print(f"  ✗ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
    
    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"Total procesadas: {total}")
    print(f"Actualizadas: {actualizadas}")
    print(f"Errores: {errores}")
    print(f"Sin cambios: {total - actualizadas - errores}")
    print("=" * 80)
    
    client.close()

if __name__ == '__main__':
    try:
        migrar_participantes_embebidos()
        print("\n✓ Migración completada exitosamente")
    except Exception as e:
        print(f"\n✗ Error durante la migración: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
