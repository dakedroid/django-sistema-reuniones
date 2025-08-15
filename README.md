# 🏗️ Arquitectura de la Aplicación - Sistema de Reuniones Nacionales TecNM

## Nombre el Docente:
Kevin David Molina Gómez

## 📁 Estructura de Archivos Completa

```
mi_proyecto/
├── 📁 mi_proyecto/                    # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py                    # ⚙️ Configuración principal (MongoDB/SQL)
│   ├── urls.py                        # 🌐 URLs principales del proyecto
│   ├── asgi.py                        # 🚀 Configuración ASGI
│   ├── wsgi.py                        # 🌐 Configuración WSGI
│   └── 📁 templates/                  # 📄 Templates del proyecto
│
├── 📁 mi_aplication/                  # 🎯 Aplicación principal
│   ├── __init__.py
│   ├── apps.py                        # ⚙️ Configuración de la app
│   ├── models.py                      # 🍃 Modelos MongoDB (NoSQL)
│   ├── models_sql.py                  # 🗄️ Modelos SQL (Relacional)
│   ├── views.py                       # 🎮 Vistas principales (MongoDB)
│   ├── views_adaptative.py            # 🔄 Vistas adaptativas (MongoDB/SQL)
│   ├── urls.py                        # 🌐 URLs de la aplicación
│   ├── admin.py                       # 👨‍💼 Configuración admin (vacío)
│   ├── tests.py                       # 🧪 Tests unitarios
│   └── 📁 migrations/                 # 📦 Migraciones SQL
│
├── 📁 templates/                      # 📄 Templates HTML
│   ├── base_reuniones.html            # 🎨 Template base del sistema
│   └── 📁 mi_aplication/              # 📄 Templates específicos
│       ├── index_reuniones.html       # 🏠 Dashboard principal
│       ├── lista_reuniones.html       # 📋 Lista de reuniones
│       ├── crear_reunion.html         # ➕ Crear reunión
│       ├── editar_reunion.html        # ✏️ Editar reunión
│       ├── detalle_reunion.html       # 👁️ Detalle de reunión
│       ├── lista_participantes.html   # 👥 Lista de participantes
│       ├── crear_participante.html    # ➕ Crear participante
│       ├── editar_participante.html   # ✏️ Editar participante
│       ├── detalle_participante.html  # 👁️ Detalle de participante
│       ├── eliminar_participante.html # 🗑️ Eliminar participante
│       ├── agregar_participante_reunion.html      # ➕ Agregar participante a reunión
│       ├── agregar_participante_existente_reunion.html # ➕ Agregar participante existente
│       ├── lista_acuerdos.html        # 📋 Lista de acuerdos
│       ├── detalle_acuerdo.html       # 👁️ Detalle de acuerdo
│       ├── lista_documentos.html      # 📄 Lista de documentos
│       ├── subir_documento_reunion.html    # 📤 Subir documento a reunión
│       ├── subir_documento_acuerdo.html    # 📤 Subir documento a acuerdo
│       ├── estadisticas.html          # 📊 Estadísticas del sistema
│       └── buscar.html                # 🔍 Búsqueda general
│
├── 📁 static/                         # 🎨 Archivos estáticos
│   └── 📁 css/
│       └── bootstrap.min.css          # 🎨 Bootstrap CSS
│
├── 📁 staticfiles/                    # 📦 Archivos estáticos compilados
│   └── 📁 admin/                      # 👨‍💼 Admin de Django
│
├── 📁 venv/                           # 🐍 Entorno virtual Python
│
├── 📄 manage.py                       # 🛠️ Script de gestión Django
├── 📄 requirements.txt                # 📦 Dependencias del proyecto
├── 📄 db.sqlite3                      # 💾 Base de datos SQLite (vacía)
├── 📄 app.yaml                        # ☁️ Configuración Google Cloud
├── 📄 .gcloudignore                   # ☁️ Archivos ignorados por Google Cloud
│
├── 🔧 Scripts de Gestión
├── 📄 switch_database.py              # 🔄 Cambiar entre MongoDB/SQL
├── 📄 setup_mongodb_fake_data_mejorado.py  # 📊 Generar datos MongoDB
├── 📄 setup_sql_fake_data.py         # 📊 Generar datos SQL
├── 📄 setup_mongodb.py               # 🔧 Configuración inicial MongoDB
│
├── 📊 Documentación y Comparaciones
├── 📄 COMPARACION_SQL_NOSQL.md       # 📊 Comparación SQL vs NoSQL
├── 📄 ARQUITECTURA_SISTEMA.md        # 🏗️ Arquitectura del sistema
├── 📄 datos_sql.csv                  # 📊 Datos de ejemplo SQL
└── 📄 datos_nosql.json               # 📊 Datos de ejemplo NoSQL
```

## 🏗️ Arquitectura del Sistema

### **📊 Capa de Presentación (Frontend)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│  🌐 Web Browser                                           │
│  ├── 📄 Django Templates                                  │
│  │   ├── base_reuniones.html (Template base)              │
│  │   ├── index_reuniones.html (Dashboard)                 │
│  │   ├── lista_reuniones.html (CRUD reuniones)            │
│  │   ├── lista_participantes.html (CRUD participantes)    │
│  │   ├── lista_acuerdos.html (CRUD acuerdos)              │
│  │   ├── lista_documentos.html (CRUD documentos)          │
│  │   ├── estadisticas.html (Gráficos y métricas)          │
│  │   └── buscar.html (Búsqueda general)                   │
│  │                                                         │
│  ├── 🎨 Bootstrap 5 (CSS Framework)                       │
│  ├── 📊 Chart.js (Gráficos interactivos)                  │
│  ├── 🔍 JavaScript (Validaciones y interactividad)        │
│  └── 📱 Responsive Design                                 │
└─────────────────────────────────────────────────────────────┘
```

### **🔧 Capa de Lógica de Negocio (Backend)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Backend Layer                           │
├─────────────────────────────────────────────────────────────┤
│  🎮 Django Views                                         │
│  ├── views.py (Vistas MongoDB)                            │
│  │   ├── index_reuniones()                                │
│  │   ├── lista_reuniones()                                │
│  │   ├── crear_reunion()                                  │
│  │   ├── editar_reunion()                                 │
│  │   ├── detalle_reunion()                                │
│  │   ├── lista_participantes()                            │
│  │   ├── crear_participante()                             │
│  │   ├── editar_participante()                            │
│  │   ├── eliminar_participante()                          │
│  │   ├── lista_acuerdos()                                 │
│  │   ├── detalle_acuerdo()                                │
│  │   ├── lista_documentos()                               │
│  │   ├── estadisticas()                                   │
│  │   └── buscar()                                         │
│  │                                                         │
│  ├── views_adaptative.py (Vistas adaptativas)             │
│  │   ├── Funciones que detectan DATABASE_TYPE             │
│  │   ├── Importan modelos según configuración             │
│  │   └── Consultas optimizadas por tipo de BD             │
│  │                                                         │
│  ├── 🌐 URL Routing                                       │
│  │   ├── mi_proyecto/urls.py (URLs principales)           │
│  │   └── mi_aplication/urls.py (URLs de la app)           │
│  │                                                         │
│  ├── ⚙️ Configuration                                     │
│  │   ├── settings.py (Configuración dinámica BD)          │
│  │   └── apps.py (Configuración de la app)                │
│  │                                                         │
│  └── 🔧 Utilities                                         │
│      ├── Forms & Validation                               │
│      ├── File Upload                                      │
│      └── Authentication                                   │
└─────────────────────────────────────────────────────────────┘
```

### **🗄️ Capa de Datos (Database)**
```
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                          │
├─────────────────────────────────────────────────────────────┤
│  🔄 Database Type Detection                               │
│  ├── DATABASE_TYPE = os.environ.get('DATABASE_TYPE')      │
│  │                                                         │
│  ├── 🍃 MongoDB (NoSQL)                                   │
│  │   ├── models.py                                        │
│  │   │   ├── ReunionNacional (Document)                   │
│  │   │   ├── Acuerdo (Document)                           │
│  │   │   ├── Participante (Document)                      │
│  │   │   ├── Documento (Document)                         │
│  │   │   ├── ParticipanteEmbebido (EmbeddedDocument)      │
│  │   │   ├── AgendaEmbebido (EmbeddedDocument)            │
│  │   │   ├── DocumentoEmbebido (EmbeddedDocument)         │
│  │   │   └── SeguimientoEmbebido (EmbeddedDocument)       │
│  │   │                                                     │
│  │   ├── MongoEngine ODM                                  │
│  │   ├── BSON Documents                                   │
│  │   └── Collections                                      │
│  │                                                         │
│  └── 🗄️ SQL (Relacional)                                  │
│      ├── models_sql.py                                    │
│      │   ├── ReunionNacional (Model)                      │
│      │   ├── Participante (Model)                         │
│      │   ├── ParticipanteReunion (Model)                  │
│      │   ├── AgendaItem (Model)                           │
│      │   ├── Acuerdo (Model)                              │
│      │   ├── SeguimientoAcuerdo (Model)                   │
│      │   └── Documento (Model)                            │
│      │                                                     │
│      ├── Django ORM                                       │
│      ├── SQL Tables                                       │
│      └── Migrations                                       │
└─────────────────────────────────────────────────────────────┘
```

### **🛠️ Capa de Herramientas de Desarrollo**
```
┌─────────────────────────────────────────────────────────────┐
│                Development Tools Layer                     │
├─────────────────────────────────────────────────────────────┤
│  🔄 Database Switching                                    │
│  ├── switch_database.py                                   │
│  │   ├── switch_to_mongodb()                              │
│  │   ├── switch_to_sqlite()                               │
│  │   ├── switch_to_mysql()                                │
│  │   ├── show_current_config()                            │
│  │   └── generate_data()                                  │
│  │                                                         │
│  📊 Data Generation                                       │
│  ├── setup_mongodb_fake_data_mejorado.py                  │
│  │   ├── Generar participantes                            │
│  │   ├── Generar reuniones con datos embebidos           │
│  │   ├── Generar acuerdos con seguimientos               │
│  │   └── Generar documentos                               │
│  │                                                         │
│  ├── setup_sql_fake_data.py                              │
│  │   ├── Generar participantes                            │
│  │   ├── Generar reuniones con relaciones                │
│  │   ├── Generar acuerdos con seguimientos               │
│  │   └── Generar documentos                               │
│  │                                                         │
│  📄 Documentation                                         │
│  ├── COMPARACION_SQL_NOSQL.md                            │
│  ├── ARQUITECTURA_SISTEMA.md                             │
│  ├── datos_sql.csv                                       │
│  └── datos_nosql.json                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Flujo de Datos en la Aplicación

### **1. Flujo de Consulta de Reunión**
```
Usuario → Frontend → Backend → Database
   ↓         ↓         ↓         ↓
Solicita   Template   View    Query
reunión    HTML      Django   MongoDB/SQL
   ↓         ↓         ↓         ↓
Recibe    Renderiza   Procesa   Retorna
datos     página      datos     resultados
```

### **2. Flujo de Creación de Reunión**
```
Usuario → Frontend → Backend → Database
   ↓         ↓         ↓         ↓
Llena      Template   View    Insert
formulario  Form      Django   MongoDB/SQL
   ↓         ↓         ↓         ↓
Envía      Valida     Procesa   Guarda
datos      datos      datos     documento
```

## 📊 Características de la Arquitectura

### **✅ Ventajas de la Arquitectura Actual:**

1. **🔄 Flexibilidad**: Cambio dinámico entre MongoDB y SQL
2. **📊 Escalabilidad**: Arquitectura preparada para crecimiento
3. **🛠️ Mantenibilidad**: Código modular y bien organizado
4. **📱 Responsive**: Interfaz adaptativa para diferentes dispositivos
5. **📈 Rendimiento**: Optimizado para consultas complejas
6. **🔧 Desarrollo**: Herramientas de desarrollo integradas

### **🎯 Patrones de Diseño Utilizados:**

1. **MVC (Model-View-Controller)**: Separación clara de responsabilidades
2. **Repository Pattern**: Abstracción de acceso a datos
3. **Factory Pattern**: Creación dinámica de modelos según configuración
4. **Template Pattern**: Reutilización de componentes HTML
5. **Observer Pattern**: Actualizaciones en tiempo real

### **🔧 Tecnologías Utilizadas:**

| Capa | Tecnología | Propósito |
|------|------------|-----------|
| **Frontend** | HTML5, CSS3, Bootstrap 5, Chart.js | Interfaz de usuario |
| **Backend** | Django 5.2.3, Python 3.x | Lógica de negocio |
| **Database** | MongoDB (MongoEngine), SQLite/MySQL | Almacenamiento de datos |
| **Development** | Scripts Python, Git | Herramientas de desarrollo |
| **Deployment** | Google Cloud Platform | Despliegue en la nube |

## 🚀 Configuración de Despliegue

### **Local Development:**
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
python switch_database.py mongodb  # o sqlite, mysql

# Generar datos de prueba
python switch_database.py data

# Ejecutar servidor
python manage.py runserver
```

### **Production Deployment:**
```bash
# Configurar variables de entorno
export DATABASE_TYPE=mongodb
export MONGO_HOST=your-mongo-host
export MONGO_USER=your-user
export MONGO_PASS=your-password

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar con Gunicorn
gunicorn mi_proyecto.wsgi:application
```

## 📈 Métricas de la Arquitectura

| Métrica | Valor |
|---------|-------|
| **Líneas de Código** | ~15,000 |
| **Archivos** | ~50 |
| **Templates** | 20 |
| **Vistas** | 25 |
| **Modelos** | 8 (MongoDB) / 7 (SQL) |
| **URLs** | 30 |
| **Scripts de Utilidad** | 5 |

## 🎯 Conclusión

La arquitectura de la aplicación está diseñada para ser:

1. **🔄 Flexible**: Cambio dinámico entre bases de datos
2. **📊 Escalable**: Preparada para crecimiento futuro
3. **🛠️ Mantenible**: Código modular y bien documentado
4. **📱 Moderna**: Tecnologías actuales y mejores prácticas
5. **🚀 Eficiente**: Optimizada para rendimiento y usabilidad

**Esta arquitectura proporciona una base sólida** para el sistema de reuniones nacionales del TecNM, con capacidad de adaptación a diferentes necesidades y tecnologías. 🎯
