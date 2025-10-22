"""
Script para migrar participantes con los nuevos campos del modelo
Actualiza registros existentes agregando datos fake donde sea necesario
"""
import os
import sys
import django
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

from mi_aplication.models import Participante
from mi_aplication.constants import PLANTELES_TECNM, AREAS_DEPARTAMENTO, SEXOS

# Datos fake para completar
DIRECTORES_FAKE = [
    "Dr. Carlos Mendoza García",
    "Dra. María Elena Torres",
    "Mtro. Roberto Sánchez López",
    "Dra. Patricia Ramírez Vega",
    "Dr. Fernando Castro Ruiz",
    "Mtra. Laura Martínez Silva",
    "Dr. José Luis Hernández"
]

JEFES_FAKE = [
    "Mtro. Juan Pérez González",
    "Dra. Ana María Flores",
    "Ing. Pedro Rodríguez Castro",
    "Mtra. Sofía López Ramírez",
    "Dr. Miguel Ángel Vargas",
    "Lic. Carmen Gómez Torres"
]

PUESTOS_FAKE = [
    "Profesor de Tiempo Completo",
    "Profesor de Asignatura",
    "Jefe de Departamento",
    "Coordinador Académico",
    "Subdirector Académico",
    "Investigador",
    "Docente Investigador"
]

def generar_rfc_fake(nombre, apellido_paterno, apellido_materno):
    """Genera un RFC fake basado en el nombre"""
    try:
        # Primeras 2 letras del apellido paterno
        ap = apellido_paterno[:2].upper() if apellido_paterno else "XX"
        # Primera letra del apellido materno
        am = apellido_materno[0].upper() if apellido_materno else "X"
        # Primera letra del nombre
        n = nombre[0].upper() if nombre else "X"
        # Fecha fake
        anio = str(random.randint(60, 99))
        mes = str(random.randint(1, 12)).zfill(2)
        dia = str(random.randint(1, 28)).zfill(2)
        # Homoclave fake
        homo = ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(3)])
        
        return f"{ap}{am}{n}{anio}{mes}{dia}{homo}"
    except:
        return "XAXX010101000"

def generar_curp_fake(rfc, sexo):
    """Genera un CURP fake basado en el RFC"""
    try:
        # Usar primeros 10 caracteres del RFC
        base = rfc[:10]
        # Sexo
        s = 'H' if sexo == 'M' else 'M' if sexo == 'F' else 'X'
        # Estado (fake)
        estado = random.choice(['DF', 'NL', 'JL', 'QT', 'SL', 'BC', 'SO'])
        # Consonantes internas (fake)
        cons = ''.join([random.choice('BCDFGHJKLMNPQRSTVWXYZ') for _ in range(3)])
        # Dígito verificador
        dig = str(random.randint(0, 9))
        
        return f"{base}{s}{estado}{cons}{dig}{dig}"
    except:
        return "XAXX010101HDFXXX00"

def migrar_participantes():
    """Migra todos los participantes existentes"""
    print("=" * 80)
    print("MIGRANDO PARTICIPANTES - ACTUALIZANDO CAMPOS")
    print("=" * 80)
    
    # Acceder directamente a la colección de MongoDB
    from pymongo import MongoClient
    from django.conf import settings
    
    # Conectar a MongoDB directamente
    client = MongoClient(settings.DATABASES['default']['host'])
    db = client[settings.DATABASES['default']['name']]
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
            
            cambios = {}
            
            # Migrar instituto -> plantel_tecnm
            if 'instituto' in doc:
                instituto_valor = doc['instituto']
                if 'plantel_tecnm' not in doc or not doc.get('plantel_tecnm'):
                    # Intentar encontrar coincidencia en el nombre
                    plantel_encontrado = None
                    instituto_lower = participante.instituto.lower()
                    
                    for codigo, nombre in PLANTELES_TECNM:
                        if nombre.lower() in instituto_lower or instituto_lower in nombre.lower():
                            plantel_encontrado = codigo
                            break
                    
                    if not plantel_encontrado:
                        # Asignar uno aleatorio
                        plantel_encontrado = random.choice(planteles_codigos)
                    
                    participante.plantel_tecnm = plantel_encontrado
                    cambios.append(f"plantel_tecnm = {plantel_encontrado}")
                
                # Eliminar campo antiguo instituto si existe
                if hasattr(participante, '_data') and 'instituto' in participante._data:
                    del participante._data['instituto']
                    cambios.append("eliminado campo 'instituto'")
            else:
                # No tiene instituto, asignar uno aleatorio
                if not hasattr(participante, 'plantel_tecnm') or not participante.plantel_tecnm:
                    participante.plantel_tecnm = random.choice(planteles_codigos)
                    cambios.append(f"plantel_tecnm = {participante.plantel_tecnm}")
            
            # Migrar departamento -> area_departamento
            if hasattr(participante, 'departamento') and participante.departamento:
                if not hasattr(participante, 'area_departamento') or not participante.area_departamento:
                    # Intentar mapear
                    area_encontrada = None
                    dept_lower = participante.departamento.lower()
                    
                    for codigo, nombre in AREAS_DEPARTAMENTO:
                        if nombre.lower() in dept_lower or dept_lower in nombre.lower():
                            area_encontrada = codigo
                            break
                    
                    if not area_encontrada:
                        area_encontrada = random.choice(areas_codigos)
                    
                    participante.area_departamento = area_encontrada
                    cambios.append(f"area_departamento = {area_encontrada}")
                
                # Eliminar campo antiguo
                if hasattr(participante, '_data') and 'departamento' in participante._data:
                    del participante._data['departamento']
                    cambios.append("eliminado campo 'departamento'")
            else:
                # Asignar área aleatoria
                if not hasattr(participante, 'area_departamento') or not participante.area_departamento:
                    participante.area_departamento = random.choice(areas_codigos)
                    cambios.append(f"area_departamento = {participante.area_departamento}")
            
            # RFC
            if not hasattr(participante, 'rfc') or not participante.rfc:
                participante.rfc = generar_rfc_fake(
                    participante.nombre,
                    participante.apellido_paterno,
                    participante.apellido_materno or ""
                )
                cambios.append(f"rfc = {participante.rfc}")
            
            # CURP
            if not hasattr(participante, 'curp') or not participante.curp:
                sexo_actual = participante.sexo if hasattr(participante, 'sexo') and participante.sexo else random.choice(sexos_valores)
                participante.curp = generar_curp_fake(participante.rfc, sexo_actual)
                cambios.append(f"curp = {participante.curp}")
            
            # Sexo
            if not hasattr(participante, 'sexo') or not participante.sexo:
                participante.sexo = random.choice(sexos_valores)
                cambios.append(f"sexo = {participante.sexo}")
            
            # Edad
            if not hasattr(participante, 'edad') or not participante.edad:
                participante.edad = random.randint(25, 65)
                cambios.append(f"edad = {participante.edad}")
            
            # Puesto
            if not hasattr(participante, 'puesto') or not participante.puesto:
                participante.puesto = random.choice(PUESTOS_FAKE)
                cambios.append(f"puesto = {participante.puesto}")
            
            # Director
            if not hasattr(participante, 'director') or not participante.director:
                participante.director = random.choice(DIRECTORES_FAKE)
                cambios.append(f"director = {participante.director}")
            
            # Correo dirección
            if not hasattr(participante, 'correo_direccion') or not participante.correo_direccion:
                participante.correo_direccion = f"direccion.{participante.plantel_tecnm.lower()}@tecnm.mx"
                cambios.append(f"correo_direccion = {participante.correo_direccion}")
            
            # Jefe inmediato
            if not hasattr(participante, 'jefe_inmediato') or not participante.jefe_inmediato:
                participante.jefe_inmediato = random.choice(JEFES_FAKE)
                cambios.append(f"jefe_inmediato = {participante.jefe_inmediato}")
            
            # Correo jefe
            if not hasattr(participante, 'correo_jefe_inmediato') or not participante.correo_jefe_inmediato:
                jefe_parts = participante.jefe_inmediato.split()
                if len(jefe_parts) >= 2:
                    correo_jefe = f"{jefe_parts[0].lower()}.{jefe_parts[-1].lower()}@tecnm.mx"
                else:
                    correo_jefe = f"jefe.{participante.plantel_tecnm.lower()}@tecnm.mx"
                participante.correo_jefe_inmediato = correo_jefe
                cambios.append(f"correo_jefe_inmediato = {correo_jefe}")
            
            # Guardar cambios
            if cambios:
                participante.save()
                actualizados += 1
                print(f"  ✓ Actualizado con {len(cambios)} cambios:")
                for cambio in cambios[:5]:  # Mostrar solo primeros 5
                    print(f"    - {cambio}")
                if len(cambios) > 5:
                    print(f"    ... y {len(cambios) - 5} más")
            else:
                print(f"  - Sin cambios necesarios")
                
        except Exception as e:
            errores += 1
            print(f"  ✗ Error: {str(e)}")
    
    print("\n" + "=" * 80)
    print("RESUMEN DE MIGRACIÓN")
    print("=" * 80)
    print(f"Total procesados: {total}")
    print(f"Actualizados: {actualizados}")
    print(f"Sin cambios: {total - actualizados - errores}")
    print(f"Errores: {errores}")
    print("=" * 80)
    
    # Verificar estructura final
    print("\nVERIFICANDO ESTRUCTURA FINAL...")
    participante_muestra = Participante.objects.first()
    if participante_muestra:
        print(f"\nMuestra de participante: {participante_muestra.nombre} {participante_muestra.apellido_paterno}")
        print(f"  - Plantel TecNM: {participante_muestra.plantel_tecnm}")
        print(f"  - Área: {participante_muestra.area_departamento}")
        print(f"  - RFC: {participante_muestra.rfc}")
        print(f"  - CURP: {participante_muestra.curp}")
        print(f"  - Sexo: {participante_muestra.sexo}")
        print(f"  - Edad: {participante_muestra.edad}")
        print(f"  - Puesto: {participante_muestra.puesto}")
        print(f"  - Director: {participante_muestra.director}")
        
        # Verificar que no existan campos antiguos
        if hasattr(participante_muestra, '_data'):
            if 'instituto' in participante_muestra._data:
                print("  ⚠ ADVERTENCIA: Campo 'instituto' aún existe")
            if 'departamento' in participante_muestra._data:
                print("  ⚠ ADVERTENCIA: Campo 'departamento' aún existe")
    
    print("\n✅ MIGRACIÓN COMPLETADA\n")

if __name__ == '__main__':
    migrar_participantes()
