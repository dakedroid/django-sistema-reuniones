#!/usr/bin/env python
"""
Script para limpiar índices problemáticos en MongoDB
"""

import os
import sys
import django
from pymongo import MongoClient

# Configurar Django
sys.path.append('/Users/molina/PycharmProjects/django-sistema-reuniones/mi_proyecto')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

def limpiar_indices():
    """Limpia los índices únicos problemáticos de MongoDB"""
    
    try:
        # Conectar a MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['tecnm_reuniones']
        
        print("🔧 Limpiando índices de la colección 'participantes'...")
        
        # Eliminar índices únicos problemáticos
        collection = db['participantes']
        
        # Listar índices existentes
        indexes = list(collection.list_indexes())
        print(f"📋 Índices encontrados: {len(indexes)}")
        
        for index in indexes:
            print(f"   - {index.get('name', 'unnamed')}: {index.get('key', {})}")
        
        # Eliminar índices problemáticos
        indices_a_eliminar = ['rfc_1', 'curp_1']
        
        for indice in indices_a_eliminar:
            try:
                collection.drop_index(indice)
                print(f"✅ Índice '{indice}' eliminado correctamente")
            except Exception as e:
                print(f"ℹ️  Índice '{indice}' no existe o ya fue eliminado: {e}")
        
        # Crear nuevos índices sparse (permiten múltiples null)
        print("🔧 Creando nuevos índices sparse...")
        
        # Índice sparse para RFC (permite múltiples null)
        try:
            collection.create_index(
                [("rfc", 1)], 
                unique=True, 
                sparse=True, 
                name="rfc_sparse"
            )
            print("✅ Índice sparse para RFC creado")
        except Exception as e:
            print(f"⚠️  Error creando índice RFC: {e}")
        
        # Índice sparse para CURP (permite múltiples null)
        try:
            collection.create_index(
                [("curp", 1)], 
                unique=True, 
                sparse=True, 
                name="curp_sparse"
            )
            print("✅ Índice sparse para CURP creado")
        except Exception as e:
            print(f"⚠️  Error creando índice CURP: {e}")
        
        # Mostrar índices finales
        print("\n📋 Índices finales:")
        indexes = list(collection.list_indexes())
        for index in indexes:
            print(f"   - {index.get('name', 'unnamed')}: {index.get('key', {})}")
        
        client.close()
        print("\n✅ ¡Limpieza de índices completada!")
        
    except Exception as e:
        print(f"❌ Error durante la limpieza: {e}")
        return False
    
    return True

def reiniciar_coleccion():
    """Opción para reiniciar completamente la colección si es necesario"""
    
    respuesta = input("\n⚠️  ¿Deseas eliminar TODOS los participantes y reiniciar la colección? (s/N): ")
    
    if respuesta.lower() in ['s', 'si', 'sí', 'yes', 'y']:
        try:
            client = MongoClient('mongodb://localhost:27017/')
            db = client['tecnm_reuniones']
            
            # Eliminar toda la colección
            db['participantes'].drop()
            print("✅ Colección 'participantes' eliminada")
            
            client.close()
            print("✅ ¡Colección reiniciada! Ahora puedes ejecutar el servidor sin problemas.")
            
        except Exception as e:
            print(f"❌ Error reiniciando colección: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🛠️  Script de Limpieza de Índices MongoDB - TecNM")
    print("=" * 50)
    
    # Intentar limpiar índices primero
    if limpiar_indices():
        print("\n✅ ¡Proceso completado! Intenta ejecutar el servidor ahora.")
    else:
        print("\n⚠️  Hubo problemas con la limpieza.")
        reiniciar_coleccion()