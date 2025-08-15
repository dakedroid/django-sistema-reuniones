#!/usr/bin/env python
"""
Script para configurar la base de datos MongoDB con datos de ejemplo
para el Sistema de Reuniones Nacionales del TecNM
"""

import os
import sys
import django
from datetime import datetime, timedelta
from bson import ObjectId

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
django.setup()

# Importar modelos después de configurar Django
from mi_aplication.models import (
    ReunionNacional, Acuerdo, Participante, Documento,
    ParticipanteEmbebido, DocumentoEmbebido, AgendaEmbebido, SeguimientoEmbebido
)

def create_admin_user():
    """Crear usuario administrador"""
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@tecnm.mx', 'admin12345')
        print("✅ Usuario administrador creado: admin/admin12345")

def create_example_reunions():
    """Crear reuniones de ejemplo con objetos anidados"""
    print("\n📅 Creando reuniones de ejemplo...")
    
    # Reunión 1: RNSA
    reunion1 = ReunionNacional(
        titulo="Reunión Nacional de Subdirectores Académicos 2024",
        tipo="RNSA",
        fecha_inicio=datetime(2024, 11, 15, 9, 0),
        fecha_fin=datetime(2024, 11, 17, 18, 0),
        sede="Instituto Tecnológico de Monterrey, Campus Ciudad de México",
        estado="PLANIFICADA",
        descripcion="Reunión anual para coordinar políticas académicas y mejorar la calidad educativa en todos los institutos del TecNM.",
        objetivos="Establecer lineamientos académicos, compartir mejores prácticas y definir estrategias para el próximo ciclo escolar.",
        participantes_esperados=150,
        presupuesto_asignado=250000.00,
        organizador_principal="Dr. María González, Subdirectora de Asuntos Académicos"
    )
    
    # Agregar participantes embebidos
    reunion1.participantes = [
        ParticipanteEmbebido(
            nombre="Juan Carlos",
            apellido_paterno="Rodríguez",
            apellido_materno="López",
            email="juan.rodriguez@tecnm.mx",
            telefono="555-123-4567",
            instituto="Instituto Tecnológico de Minatitlán",
            departamento="Subdirección Académica",
            tipo_participante="SUBDIRECTOR",
            confirmado=True,
            fecha_confirmacion=datetime.now(),
            observaciones="Participante confirmado con hotel reservado"
        ),
        ParticipanteEmbebido(
            nombre="Ana María",
            apellido_paterno="García",
            apellido_materno="Hernández",
            email="ana.garcia@tecnm.mx",
            telefono="555-987-6543",
            instituto="Instituto Tecnológico de Villahermosa",
            departamento="Subdirección Académica",
            tipo_participante="SUBDIRECTOR",
            confirmado=True,
            fecha_confirmacion=datetime.now(),
            observaciones="Requiere dieta especial"
        ),
        ParticipanteEmbebido(
            nombre="Carlos",
            apellido_paterno="Martínez",
            apellido_materno="Pérez",
            email="carlos.martinez@tecnm.mx",
            telefono="555-456-7890",
            instituto="Instituto Tecnológico de Coatzacoalcos",
            departamento="Subdirección Académica",
            tipo_participante="SUBDIRECTOR",
            confirmado=False,
            observaciones="Pendiente de confirmación"
        )
    ]
    
    # Agregar agenda embebida
    reunion1.agenda = [
        AgendaEmbebido(
            titulo="Inauguración y Bienvenida",
            descripcion="Ceremonia de apertura con autoridades del TecNM",
            hora_inicio="09:00",
            hora_fin="10:30",
            responsable="Dr. María González",
            tipo_actividad="PRESENTACION"
        ),
        AgendaEmbebido(
            titulo="Presentación de Nuevas Políticas Académicas",
            descripcion="Revisión de lineamientos actualizados para el ciclo 2024-2025",
            hora_inicio="11:00",
            hora_fin="13:00",
            responsable="Mtra. Laura Sánchez",
            tipo_actividad="PRESENTACION"
        ),
        AgendaEmbebido(
            titulo="Trabajo en Grupos por Región",
            descripcion="Discusión de problemáticas específicas por región geográfica",
            hora_inicio="15:00",
            hora_fin="17:30",
            responsable="Coordinadores Regionales",
            tipo_actividad="TRABAJO_GRUPO"
        )
    ]
    
    # Agregar documentos embebidos
    reunion1.documentos = [
        DocumentoEmbebido(
            titulo="Programa General RNSA 2024",
            descripcion="Programa detallado de actividades para los tres días",
            tipo="AGENDA",
            url="https://drive.google.com/file/d/example1",
            formato="pdf",
            tamaño=2048576,
            version="1.0",
            fecha_subida=datetime.now(),
            subido_por="Sistema",
            observaciones="Documento oficial de la reunión"
        ),
        DocumentoEmbebido(
            titulo="Nuevas Políticas Académicas 2024-2025",
            descripcion="Documento con las políticas actualizadas",
            tipo="MEMORANDUM",
            url="https://drive.google.com/file/d/example2",
            formato="docx",
            tamaño=1536000,
            version="2.1",
            fecha_subida=datetime.now(),
            subido_por="Dr. María González",
            observaciones="Versión final aprobada"
        )
    ]
    
    reunion1.save()
    print(f"✅ Reunión creada: {reunion1.titulo}")
    
    # Reunión 2: RNPD
    reunion2 = ReunionNacional(
        titulo="Reunión Nacional de Posgrado y Desarrollo 2024",
        tipo="RNPD",
        fecha_inicio=datetime(2024, 12, 5, 8, 30),
        fecha_fin=datetime(2024, 12, 7, 17, 0),
        sede="Instituto Tecnológico de Querétaro",
        estado="EN_CURSO",
        descripcion="Reunión para fortalecer los programas de posgrado y fomentar la investigación en el TecNM.",
        objetivos="Mejorar la calidad de los posgrados, establecer colaboraciones de investigación y definir estrategias de desarrollo.",
        participantes_esperados=80,
        presupuesto_asignado=180000.00,
        organizador_principal="Dr. Roberto Silva, Director de Posgrado"
    )
    
    # Agregar participantes embebidos
    reunion2.participantes = [
        ParticipanteEmbebido(
            nombre="Dr. Patricia",
            apellido_paterno="López",
            apellido_materno="Mendoza",
            email="patricia.lopez@tecnm.mx",
            telefono="555-111-2222",
            instituto="Instituto Tecnológico de Minatitlán",
            departamento="Coordinación de Posgrado",
            tipo_participante="COORDINADOR",
            confirmado=True,
            fecha_confirmacion=datetime.now(),
            observaciones="Presentará ponencia sobre nuevos programas"
        )
    ]
    
    reunion2.save()
    print(f"✅ Reunión creada: {reunion2.titulo}")
    
    return reunion1, reunion2

def create_example_acuerdos(reunion1, reunion2):
    """Crear acuerdos de ejemplo con objetos anidados"""
    print("\n🤝 Creando acuerdos de ejemplo...")
    
    # Acuerdo 1
    acuerdo1 = Acuerdo(
        titulo="Implementación de Nuevas Políticas Académicas",
        descripcion="Implementar las nuevas políticas académicas en todos los institutos del TecNM para el ciclo 2024-2025.",
        categoria="ACADEMICA",
        estado="EN_PROCESO",
        prioridad="ALTA",
        reunion=reunion1,
        responsable="Dr. María González",
        fecha_limite=datetime(2025, 2, 28),
        seguimientos=[
            SeguimientoEmbebido(
                fecha_seguimiento=datetime.now() - timedelta(days=30),
                estado_anterior="PENDIENTE",
                estado_nuevo="EN_PROCESO",
                porcentaje_avance=25,
                observaciones="Se han enviado las políticas a todos los institutos para revisión",
                responsable="Dr. María González"
            ),
            SeguimientoEmbebido(
                fecha_seguimiento=datetime.now() - timedelta(days=15),
                estado_anterior="EN_PROCESO",
                estado_nuevo="EN_PROCESO",
                porcentaje_avance=50,
                observaciones="Se han recibido comentarios de 45 institutos, pendientes 15",
                responsable="Dr. María González"
            )
        ],
        documentos=[
            DocumentoEmbebido(
                titulo="Políticas Académicas Finales",
                descripcion="Versión final de las políticas a implementar",
                tipo="MEMORANDUM",
                url="https://drive.google.com/file/d/acuerdo1",
                formato="pdf",
                tamaño=3072000,
                version="3.0",
                fecha_subida=datetime.now(),
                subido_por="Dr. María González"
            )
        ]
    )
    acuerdo1.save()
    print(f"✅ Acuerdo creado: {acuerdo1.titulo}")
    
    # Acuerdo 2
    acuerdo2 = Acuerdo(
        titulo="Fortalecimiento de Programas de Posgrado",
        descripcion="Mejorar la calidad y acreditación de los programas de posgrado en el TecNM.",
        categoria="ACADEMICA",
        estado="PENDIENTE",
        prioridad="MEDIA",
        reunion=reunion2,
        responsable="Dr. Roberto Silva",
        fecha_limite=datetime(2025, 6, 30),
        seguimientos=[
            SeguimientoEmbebido(
                fecha_seguimiento=datetime.now() - timedelta(days=5),
                estado_anterior="PENDIENTE",
                estado_nuevo="PENDIENTE",
                porcentaje_avance=0,
                observaciones="Acuerdo recién establecido, pendiente de iniciar acciones",
                responsable="Dr. Roberto Silva"
            )
        ]
    )
    acuerdo2.save()
    print(f"✅ Acuerdo creado: {acuerdo2.titulo}")
    
    return acuerdo1, acuerdo2

def create_example_participantes():
    """Crear participantes independientes de ejemplo"""
    print("\n👥 Creando participantes independientes...")
    
    participante1 = Participante(
        nombre="Dr. Francisco",
        apellido_paterno="Hernández",
        apellido_materno="García",
        email="francisco.hernandez@tecnm.mx",
        telefono="555-333-4444",
        instituto="Instituto Tecnológico de Minatitlán",
        departamento="Dirección General",
        tipo_participante="DIRECTOR",
        confirmado=True,
        fecha_confirmacion=datetime.now(),
        observaciones="Director con amplia experiencia en gestión académica"
    )
    participante1.save()
    print(f"✅ Participante creado: {participante1}")
    
    participante2 = Participante(
        nombre="Mtra. Carmen",
        apellido_paterno="Vargas",
        apellido_materno="Ruiz",
        email="carmen.vargas@tecnm.mx",
        telefono="555-555-6666",
        instituto="Instituto Tecnológico de Villahermosa",
        departamento="Subdirección Académica",
        tipo_participante="SUBDIRECTOR",
        confirmado=True,
        fecha_confirmacion=datetime.now(),
        observaciones="Especialista en innovación educativa"
    )
    participante2.save()
    print(f"✅ Participante creado: {participante2}")

def create_example_documents():
    """Crear documentos independientes de ejemplo"""
    print("\n📄 Creando documentos independientes...")
    
    documento1 = Documento(
        titulo="Manual de Procedimientos Académicos 2024",
        descripcion="Manual actualizado con todos los procedimientos académicos del TecNM",
        tipo="MEMORANDUM",
        url="https://drive.google.com/file/d/doc1",
        formato="pdf",
        tamaño=5120000,
        version="4.2",
        fecha_subida=datetime.now(),
        subido_por="Sistema",
        observaciones="Documento de referencia para todas las reuniones"
    )
    documento1.save()
    print(f"✅ Documento creado: {documento1.titulo}")
    
    documento2 = Documento(
        titulo="Estadísticas Académicas 2023-2024",
        descripcion="Reporte estadístico del desempeño académico del TecNM",
        tipo="ACTA",
        url="https://drive.google.com/file/d/doc2",
        formato="xlsx",
        tamaño=2048000,
        version="1.0",
        fecha_subida=datetime.now(),
        subido_por="Dr. María González",
        observaciones="Datos para análisis en reuniones"
    )
    documento2.save()
    print(f"✅ Documento creado: {documento2.titulo}")

def main():
    """Función principal para configurar la base de datos"""
    print("🚀 Configurando Sistema de Reuniones Nacionales del TecNM")
    print("=" * 60)
    
    try:
        # Crear usuario administrador
        create_admin_user()
        
        # Crear datos de ejemplo
        reunion1, reunion2 = create_example_reunions()
        acuerdo1, acuerdo2 = create_example_acuerdos(reunion1, reunion2)
        create_example_participantes()
        create_example_documents()
        
        print("\n" + "=" * 60)
        print("✅ Configuración completada exitosamente!")
        print("\n📋 Resumen de datos creados:")
        print(f"   • Reuniones: {ReunionNacional.objects.count()}")
        print(f"   • Acuerdos: {Acuerdo.objects.count()}")
        print(f"   • Participantes: {Participante.objects.count()}")
        print(f"   • Documentos: {Documento.objects.count()}")
        
        print("\n🌐 Acceso al sistema:")
        print("   • URL principal: http://localhost:8000/")
        print("   • Dashboard: http://localhost:8000/mi_aplication/")
        print("   • Admin Django: http://localhost:8000/admin/")
        print("   • Usuario admin: admin / admin12345")
        
        print("\n📊 Características del nuevo sistema:")
        print("   • Modelos con objetos anidados (embebidos)")
        print("   • Referencias entre documentos")
        print("   • Estructura optimizada para MongoDB")
        print("   • Sistema de seguimiento de acuerdos")
        print("   • Gestión de participantes y documentos")
        
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
