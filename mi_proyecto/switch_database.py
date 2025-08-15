#!/usr/bin/env python3
"""
Script para cambiar entre diferentes tipos de base de datos
Uso: python switch_database.py [mongodb|sqlite|mysql]
"""

import os
import sys
import subprocess
from pathlib import Path

def switch_to_mongodb():
    """Cambiar a MongoDB"""
    print("🔄 Cambiando a MongoDB...")
    
    # Configurar variables de entorno
    os.environ['DATABASE_TYPE'] = 'mongodb'
    os.environ['MONGO_HOST'] = '127.0.0.1'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_USER'] = 'admin'
    os.environ['MONGO_PASS'] = 'admin12345'
    os.environ['MONGO_AUTH_SOURCE'] = 'admin'
    os.environ['MONGO_AUTH_MECH'] = 'SCRAM-SHA-1'
    
    print("✅ Configurado para MongoDB")
    print("📊 Base de datos: tecnm_reuniones")
    print("🌐 Host: 127.0.0.1:27017")
    print("👤 Usuario: admin")
    
    # Verificar conexión
    try:
        import mongoengine
        mongoengine.connect(
            db='tecnm_reuniones',
            host='127.0.0.1',
            port=27017,
            username='admin',
            password='admin12345',
            authentication_source='admin',
            authentication_mechanism='SCRAM-SHA-1'
        )
        print("✅ Conexión a MongoDB exitosa")
    except Exception as e:
        print(f"❌ Error conectando a MongoDB: {e}")
        print("💡 Asegúrate de que MongoDB esté ejecutándose")

def switch_to_sqlite():
    """Cambiar a SQLite"""
    print("🔄 Cambiando a SQLite...")
    
    # Configurar variables de entorno
    os.environ['DATABASE_TYPE'] = 'sqlite'
    
    print("✅ Configurado para SQLite")
    print("📊 Base de datos: db.sqlite3")
    print("💾 Archivo local en el proyecto")
    
    # Crear migraciones si no existen
    try:
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Migraciones aplicadas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con migraciones: {e}")

def switch_to_mysql():
    """Cambiar a MySQL"""
    print("🔄 Cambiando a MySQL...")
    
    # Configurar variables de entorno
    os.environ['DATABASE_TYPE'] = 'mysql'
    os.environ['MYSQL_DB'] = 'tecnm_reuniones'
    os.environ['MYSQL_USER'] = 'root'
    os.environ['MYSQL_PASSWORD'] = ''
    os.environ['MYSQL_HOST'] = 'localhost'
    os.environ['MYSQL_PORT'] = '3306'
    
    print("✅ Configurado para MySQL")
    print("📊 Base de datos: tecnm_reuniones")
    print("🌐 Host: localhost:3306")
    print("👤 Usuario: root")
    
    # Crear migraciones si no existen
    try:
        subprocess.run(['python', 'manage.py', 'makemigrations'], check=True)
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        print("✅ Migraciones aplicadas")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con migraciones: {e}")

def show_current_config():
    """Mostrar configuración actual"""
    database_type = os.environ.get('DATABASE_TYPE', 'mongodb')
    print(f"📋 Configuración actual: {database_type.upper()}")
    
    if database_type == 'mongodb':
        print(f"🌐 Host: {os.environ.get('MONGO_HOST', '127.0.0.1')}")
        print(f"🔌 Puerto: {os.environ.get('MONGO_PORT', '27017')}")
        print(f"👤 Usuario: {os.environ.get('MONGO_USER', 'admin')}")
    elif database_type == 'sqlite':
        print("💾 Archivo: db.sqlite3")
    elif database_type == 'mysql':
        print(f"🌐 Host: {os.environ.get('MYSQL_HOST', 'localhost')}")
        print(f"🔌 Puerto: {os.environ.get('MYSQL_PORT', '3306')}")
        print(f"👤 Usuario: {os.environ.get('MYSQL_USER', 'root')}")

def generate_data():
    """Generar datos de prueba según el tipo de base de datos"""
    database_type = os.environ.get('DATABASE_TYPE', 'mongodb')
    
    if database_type == 'mongodb':
        print("📊 Generando datos para MongoDB...")
        subprocess.run(['python', 'setup_mongodb_fake_data_mejorado.py'])
    else:
        print("📊 Generando datos para SQL...")
        subprocess.run(['python', 'setup_sql_fake_data.py'])

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("🔧 Script para cambiar entre bases de datos")
        print("")
        print("Uso:")
        print("  python switch_database.py mongodb  # Cambiar a MongoDB")
        print("  python switch_database.py sqlite   # Cambiar a SQLite")
        print("  python switch_database.py mysql    # Cambiar a MySQL")
        print("  python switch_database.py status   # Ver configuración actual")
        print("  python switch_database.py data     # Generar datos de prueba")
        print("")
        show_current_config()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'mongodb':
        switch_to_mongodb()
    elif command == 'sqlite':
        switch_to_sqlite()
    elif command == 'mysql':
        switch_to_mysql()
    elif command == 'status':
        show_current_config()
    elif command == 'data':
        generate_data()
    else:
        print(f"❌ Comando no válido: {command}")
        print("Comandos válidos: mongodb, sqlite, mysql, status, data")

if __name__ == '__main__':
    main()
