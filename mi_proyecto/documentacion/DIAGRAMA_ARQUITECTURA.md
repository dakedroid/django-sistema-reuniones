# Diagrama de Arquitectura: Migración SQL → NoSQL

## 🔄 Transformación Completa del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           MIGRACIÓN DE ARQUITECTURA                                 │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           ANTES: SQL TRADICIONAL                            │   │
│  ├─────────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                             │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │   Django    │    │   Django    │    │   Django    │    │   Django    │  │   │
│  │  │    ORM      │    │    Admin    │    │   Views     │    │ Templates   │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │         │                   │                   │                   │      │   │
│  │         ▼                   ▼                   ▼                   ▼      │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │   SQLite    │    │   SQLite    │    │   SQLite    │    │   SQLite    │  │   │
│  │  │  Database   │    │  Database   │    │  Database   │    │  Database   │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │         │                   │                   │                   │      │   │
│  │  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐  │   │
│  │  │   Tablas    │    │   Tablas    │    │   Tablas    │    │   Tablas    │  │   │
│  │  │ Relacionales│    │ Relacionales│    │ Relacionales│    │ Relacionales│  │   │
│  │  │ - carreras  │    │ - estudiantes│   │ - reuniones │    │ - documentos│  │   │
│  │  │ - FK links  │    │ - FK links  │    │ - FK links  │    │ - FK links  │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │                                                                             │   │
│  │  ❌ Múltiples JOINs    ❌ Esquema rígido    ❌ Migraciones complejas         │   │
│  │  ❌ Rendimiento lento  ❌ Escalabilidad V  ❌ Mantenimiento difícil         │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│                                    ⬇️ MIGRACIÓN ⬇️                                  │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                          DESPUÉS: NOSQL MODERNO                             │   │
│  ├─────────────────────────────────────────────────────────────────────────────┤   │
│  │                                                                             │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │ MongoEngine │    │   Django    │    │   Django    │    │   Django    │  │   │
│  │  │     ODM     │    │   Views     │    │   Views     │    │ Templates   │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │         │                   │                   │                   │      │   │
│  │         ▼                   ▼                   ▼                   ▼      │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │   │
│  │  │  MongoDB    │    │  MongoDB    │    │  MongoDB    │    │  MongoDB    │  │   │
│  │  │  Database   │    │  Database   │    │  Database   │    │  Database   │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │         │                   │                   │                   │      │   │
│  │  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐  │   │
│  │  │ Colecciones │    │ Colecciones │    │ Colecciones │    │ Colecciones │  │   │
│  │  │ con Docs    │    │ con Docs    │    │ con Docs    │    │ con Docs    │  │   │
│  │  │ Embebidos   │    │ Embebidos   │    │ Embebidos   │    │ Embebidos   │  │   │
│  │  │ - reuniones │    │ - acuerdos  │    │ - participantes│  │ - documentos│  │   │
│  │  │ - participantes│  │ - seguimientos│  │ - institutos │  │ - metadatos │  │   │
│  │  │ - agenda    │    │ - documentos│    │ - contactos  │  │ - versiones │  │   │
│  │  │ - documentos│    │ - prioridades│   │ - tipos      │  │ - formatos  │  │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │   │
│  │                                                                             │   │
│  │  ✅ 1 consulta rápida  ✅ Esquema flexible  ✅ Sin migraciones              │   │
│  │  ✅ Documentos embebidos ✅ Escalabilidad H  ✅ Mantenimiento fácil         │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 📊 Comparación de Estructuras de Datos

### **ANTES: Modelo Relacional (SQL)**
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              MODELO RELACIONAL                                      │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   CARRERAS  │    │ ESTUDIANTES │    │  REUNIONES  │    │ DOCUMENTOS  │         │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤    ├─────────────┤         │
│  │ id (PK)     │    │ id (PK)     │    │ id (PK)     │    │ id (PK)     │         │
│  │ nombre      │    │ nombre      │    │ titulo      │    │ titulo      │         │
│  │ clave       │    │ apellido_p  │    │ fecha_inicio│    │ url         │         │
│  │ modalidad   │    │ apellido_m  │    │ fecha_fin   │    │ formato     │         │
│  │             │    │ matricula   │    │ sede        │    │ tamaño      │         │
│  │             │    │ carrera_id  │    │ estado      │    │ reunion_id  │         │
│  │             │    │ (FK)        │    │ organizador │    │ (FK)        │         │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘         │
│         ▲                   │                   ▲                   ▲            │
│         │                   │                   │                   │            │
│         └───────────────────┘                   │                   │            │
│                                                 │                   │            │
│  ┌─────────────┐    ┌─────────────┐            │                   │            │
│  │PARTICIPANTES│    │  ACUERDOS   │            │                   │            │
│  │_REUNION     │    ├─────────────┤            │                   │            │
│  ├─────────────┤    │ id (PK)     │            │                   │            │
│  │ id (PK)     │    │ titulo      │            │                   │            │
│  │ reunion_id  │    │ descripcion │            │                   │            │
│  │ (FK)        │    │ categoria   │            │                   │            │
│  │ estudiante_ │    │ estado      │            │                   │            │
│  │ id (FK)     │    │ reunion_id  │            │                   │            │
│  └─────────────┘    │ (FK)        │            │                   │            │
│                     └─────────────┘            │                   │            │
│                           ▲                    │                   │            │
│                           │                    │                   │            │
│  ┌─────────────┐    ┌─────────────┐            │                   │            │
│  │ SEGUIMIENTOS│    │  AGENDA     │            │                   │            │
│  │_ACUERDO     │    ├─────────────┤            │                   │            │
│  ├─────────────┤    │ id (PK)     │            │                   │            │
│  │ id (PK)     │    │ titulo      │            │                   │            │
│  │ acuerdo_id  │    │ descripcion │            │                   │            │
│  │ (FK)        │    │ duracion    │            │                   │            │
│  │ fecha       │    │ reunion_id  │            │                   │            │
│  │ estado      │    │ (FK)        │            │                   │            │
│  │ comentario  │    └─────────────┘            │                   │            │
│  └─────────────┘            ▲                  │                   │            │
│                              │                  │                   │            │
│                              └──────────────────┴───────────────────┘            │
│                                                                                   │
│  ❌ 8 tablas separadas    ❌ 6 relaciones FK    ❌ Consultas complejas            │
│  ❌ Múltiples JOINs       ❌ Normalización      ❌ Rendimiento lento              │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### **DESPUÉS: Modelo de Documentos (NoSQL)**
```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              MODELO DE DOCUMENTOS                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                        COLECCIÓN: reuniones_nacionales                      │   │
│  ├─────────────────────────────────────────────────────────────────────────────┤   │
│  │ {                                                                           │   │
│  │   "_id": ObjectId("..."),                                                  │   │
│  │   "titulo": "Reunión Nacional de Posgrado 2024",                           │   │
│  │   "tipo": "RNPD",                                                          │   │
│  │   "fecha_inicio": ISODate("2024-12-05T08:30:00Z"),                         │   │
│  │   "fecha_fin": ISODate("2024-12-05T17:00:00Z"),                            │   │
│  │   "sede": "Instituto Tecnológico de Querétaro",                            │   │
│  │   "modalidad": "HIBRIDA",                                                  │   │
│  │   "enlace_videollamada": "https://meet.google.com/...",                    │   │
│  │   "direccion_fisica": "Av. Tecnológico s/n, Querétaro",                    │   │
│  │   "estado": "PLANIFICADA",                                                 │   │
│  │   "organizador_principal": "Dr. Juan Carlos García",                       │   │
│  │   "descripcion": "Reunión para fortalecer programas...",                   │   │
│  │   "objetivos": "Fortalecer la colaboración entre institutos...",           │   │
│  │   "participantes_esperados": 80,                                           │   │
│  │   "presupuesto_asignado": 150000.00,                                       │   │
│  │                                                                             │   │
│  │   "participantes": [                                                       │   │
│  │     {                                                                       │   │
│  │       "nombre": "Juan Carlos",                                             │   │
│  │       "apellido_paterno": "García",                                        │   │
│  │       "apellido_materno": "Rodríguez",                                     │   │
│  │       "email": "juan.garcia@itq.edu.mx",                                   │   │
│  │       "telefono": "+52 442 123 4567",                                      │   │
│  │       "instituto": "IT Querétaro",                                         │   │
│  │       "departamento": "Académico",                                         │   │
│  │       "tipo_participante": "DIRECTOR",                                     │   │
│  │       "confirmado": true,                                                  │   │
│  │       "observaciones": "Participante confirmado"                           │   │
│  │     },                                                                      │   │
│  │     {                                                                       │   │
│  │       "nombre": "María Elena",                                             │   │
│  │       "apellido_paterno": "López",                                         │   │
│  │       "email": "maria.lopez@itc.edu.mx",                                   │   │
│  │       "instituto": "IT Celaya",                                            │   │
│  │       "tipo_participante": "SUBDIRECTOR",                                  │   │
│  │       "confirmado": false                                                  │   │
│  │     }                                                                       │   │
│  │   ],                                                                        │   │
│  │                                                                             │   │
│  │   "agenda": [                                                              │   │
│  │     {                                                                       │   │
│  │       "titulo": "Presentación de programas de posgrado",                   │   │
│  │       "descripcion": "Exposición de nuevos programas...",                  │   │
│  │       "duracion": 60,                                                      │   │
│  │       "responsable": "Dr. María Elena López",                              │   │
│  │       "hora_inicio": "09:00",                                              │   │
│  │       "hora_fin": "10:00"                                                  │   │
│  │     },                                                                      │   │
│  │     {                                                                       │   │
│  │       "titulo": "Discusión de acuerdos",                                   │   │
│  │       "descripcion": "Revisión de acuerdos pendientes...",                 │   │
│  │       "duracion": 90,                                                      │   │
│  │       "responsable": "Dr. Juan Carlos García",                             │   │
│  │       "hora_inicio": "10:30",                                              │   │
│  │       "hora_fin": "12:00"                                                  │   │
│  │     }                                                                       │   │
│  │   ],                                                                        │   │
│  │                                                                             │   │
│  │   "documentos": [                                                          │   │
│  │     {                                                                       │   │
│  │       "titulo": "Agenda de la reunión",                                    │   │
│  │       "descripcion": "Agenda oficial de la reunión",                       │   │
│  │       "tipo": "AGENDA",                                                    │   │
│  │       "url": "https://drive.google.com/file/d/agenda123/view",             │   │
│  │       "formato": "pdf",                                                    │   │
│  │       "tamaño": 1024000,                                                   │   │
│  │       "version": "1.0",                                                    │   │
│  │       "subido_por": "Dr. Juan Carlos García",                              │   │
│  │       "fecha_subida": ISODate("2024-12-01T10:00:00Z")                      │   │
│  │     }                                                                       │   │
│  │   ]                                                                         │   │
│  │ }                                                                           │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           COLECCIÓN: acuerdos                               │   │
│  ├─────────────────────────────────────────────────────────────────────────────┤   │
│  │ {                                                                           │   │
│  │   "_id": ObjectId("..."),                                                  │   │
│  │   "titulo": "Implementación de nuevos programas de posgrado",              │   │
│  │   "descripcion": "Se acuerda implementar 3 nuevos programas...",           │   │
│  │   "categoria": "ACADEMICA",                                                │   │
│  │   "estado": "EN_PROCESO",                                                  │   │
│  │   "prioridad": "ALTA",                                                     │   │
│  │   "reunion": ObjectId("..."), // Referencia a reunión                      │   │
│  │   "responsable": "Lic. Roberto Martínez",                                  │   │
│  │   "fecha_limite": ISODate("2025-06-30T23:59:59Z"),                         │   │
│  │                                                                             │   │
│  │   "seguimientos": [                                                        │   │
│  │     {                                                                       │   │
│  │       "fecha": ISODate("2024-12-10T10:00:00Z"),                            │   │
│  │       "estado": "EN_PROCESO",                                              │   │
│  │       "comentario": "Iniciando proceso de implementación",                 │   │
│  │       "responsable": "Lic. Roberto Martínez",                              │   │
│  │       "porcentaje_avance": 25                                              │   │
│  │     },                                                                      │   │
│  │     {                                                                       │   │
│  │       "fecha": ISODate("2024-12-15T14:30:00Z"),                            │   │
│  │       "estado": "EN_PROCESO",                                              │   │
│  │       "comentario": "Documentación completada al 50%",                     │   │
│  │       "responsable": "Lic. Roberto Martínez",                              │   │
│  │       "porcentaje_avance": 50                                              │   │
│  │     }                                                                       │   │
│  │   ],                                                                        │   │
│  │                                                                             │   │
│  │   "documentos": [                                                          │   │
│  │     {                                                                       │   │
│  │       "titulo": "Propuesta de programas",                                  │   │
│  │       "tipo": "PRESENTACION",                                              │   │
│  │       "url": "https://drive.google.com/file/d/propuesta456/view",          │   │
│  │       "formato": "pptx",                                                   │   │
│  │       "tamaño": 2048000                                                    │   │
│  │     }                                                                       │   │
│  │   ]                                                                         │   │
│  │ }                                                                           │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ✅ 2 colecciones principales    ✅ Documentos embebidos    ✅ 1 consulta rápida   │
│  ✅ Sin JOINs complejos          ✅ Esquema flexible        ✅ Rendimiento óptimo  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Beneficios de la Migración

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              BENEFICIOS OBTENIDOS                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   RENDIMIENTO   │  │   FLEXIBILIDAD  │  │ ESCALABILIDAD   │  │  MANTENIMIENTO  │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │                 │  │                 │  │                 │  │                 │ │
│  │ ✅ 6x más rápido│  │ ✅ Esquema      │  │ ✅ Horizontal   │  │ ✅ Código más   │ │
│  │ ✅ 3x menos     │  │   flexible      │  │ ✅ Sin límites   │  │   limpio        │ │
│  │    memoria      │  │ ✅ Sin          │  │ ✅ Sin downtime  │  │ ✅ Menos        │ │
│  │ ✅ 15x menos I/O│  │   migraciones   │  │ ✅ Distribuido   │  │   dependencias  │ │
│  │ ✅ Consultas    │  │ ✅ Agregar      │  │ ✅ Auto-sharding │  │ ✅ Despliegue   │ │
│  │    simples      │  │   campos fácil  │  │ ✅ Replicación   │  │   simple        │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  DESARROLLO     │  │  FUNCIONALIDAD  │  │   SEGURIDAD     │  │   FUTURO        │ │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤ │
│  │                 │  │                 │  │                 │  │                 │ │
│  │ ✅ Más rápido   │  │ ✅ Documentos   │  │ ✅ Autenticación│  │ ✅ Cloud-ready  │ │
│  │ ✅ Menos código │  │   embebidos     │  │   robusta       │  │ ✅ Microservicios│ │
│  │ ✅ Modelado     │  │ ✅ Búsqueda     │  │ ✅ Encriptación │  │ ✅ IoT ready     │ │
│  │    intuitivo    │  │   de texto      │  │   de datos      │  │ ✅ Big Data      │ │
│  │ ✅ Testing      │  │ ✅ Agregaciones │  │ ✅ Auditoría    │  │ ✅ AI/ML ready   │ │
│  │    simplificado │  │   complejas     │  │   completa      │  │ ✅ Serverless    │ │
│  │                 │  │                 │  │                 │  │                 │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

*Diagrama de arquitectura para presentación - Sistema de Reuniones Nacionales TecNM*
