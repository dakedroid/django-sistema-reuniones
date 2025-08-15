# Sistema de Reuniones Nacionales del TecNM

Sistema web para la gestión integral de reuniones nacionales del Tecnológico Nacional de México (TecNM), migrado a MongoDB para mayor flexibilidad y escalabilidad.

## 🚀 Características Principales

- **Gestión de Reuniones Nacionales**: Creación, edición y seguimiento de reuniones
- **Agendas Detalladas**: Programación de sesiones y actividades
- **Sistema de Acuerdos**: Seguimiento de acuerdos y compromisos
- **Gestión de Participantes**: Registro y confirmación de asistentes
- **Documentos Digitales**: Almacenamiento y gestión de memorias y presentaciones
- **Estadísticas y Reportes**: Dashboard con métricas y gráficos
- **Búsqueda Avanzada**: Búsqueda en tiempo real en todo el sistema
- **Interfaz Moderna**: Diseño responsivo con colores institucionales del TecNM

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.2.3
- **Base de Datos**: MongoDB (djongo)
- **Frontend**: Bootstrap 5, Font Awesome
- **Gráficos**: Chart.js
- **Autenticación**: Django Auth

## 📋 Requisitos Previos

- Python 3.8+
- MongoDB 4.4+
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar el Repositorio
```bash
git clone <url-del-repositorio>
cd mi_proyecto
```

### 2. Crear Entorno Virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar MongoDB

Asegúrate de que MongoDB esté ejecutándose en tu sistema:

```bash
# En macOS con Homebrew
brew services start mongodb-community

# En Ubuntu/Debian
sudo systemctl start mongod

# En Windows
net start MongoDB
```

### 5. Configurar Base de Datos

El sistema está configurado para conectarse a MongoDB con las siguientes credenciales:
- **Host**: 127.0.0.1
- **Puerto**: 27017
- **Usuario**: admin
- **Contraseña**: admin12345
- **Base de datos**: tecnm_reuniones

Si necesitas cambiar estas configuraciones, edita el archivo `mi_proyecto/settings.py`.

### 6. Ejecutar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear Datos de Ejemplo
```bash
python setup_mongodb.py
```

### 8. Ejecutar el Servidor
```bash
python manage.py runserver
```

## 🌐 Acceso al Sistema

### Sistema Principal
- **URL**: http://localhost:8000/mi_aplication/
- **Usuario**: admin
- **Contraseña**: admin12345

### Panel de Administración
- **URL**: http://localhost:8000/admin/
- **Usuario**: admin
- **Contraseña**: admin12345

## 📊 Estructura del Sistema

### Modelos Principales

1. **ReunionNacional**: Gestión de reuniones
   - Tipos: RNSA, RNPD, RNVE, RNCA, OTRA
   - Estados: Planificada, En Curso, Finalizada, Cancelada

2. **Agenda**: Programación de sesiones
   - Orden de actividades
   - Ponentes y salas
   - Horarios detallados

3. **Acuerdo**: Seguimiento de acuerdos
   - Categorías: Académico, Administrativo, Financiero, etc.
   - Estados: Pendiente, En Proceso, Completado, Cancelado

4. **Participante**: Gestión de asistentes
   - Tipos: Subdirector Académico, Director, Docente, etc.
   - Confirmación de asistencia

5. **Documento**: Archivos relacionados
   - Tipos: Memoria, Presentación, Acta, Programa, etc.

6. **SeguimientoAcuerdo**: Seguimiento de acuerdos
   - Avance porcentual
   - Obstáculos y acciones

### Funcionalidades Principales

#### Dashboard
- Estadísticas generales
- Próximas reuniones
- Acuerdos recientes
- Gráficos de rendimiento

#### Gestión de Reuniones
- Crear nueva reunión
- Editar información
- Gestionar agenda
- Asignar participantes

#### Sistema de Acuerdos
- Crear acuerdos
- Asignar responsables
- Seguimiento de avances
- Reportes de cumplimiento

#### Gestión de Participantes
- Registro de asistentes
- Confirmación de asistencia
- Listas de participantes
- Comunicaciones

#### Documentos
- Subir archivos
- Categorización
- Control de versiones
- Descargas

## 🎨 Colores Institucionales

El sistema utiliza los colores oficiales del TecNM:
- **Azul Principal**: #1E3A8A / #1F4E99
- **Verde Secundario**: #16A34A / #22C55E
- **Naranja/Coral**: #F97316 / #FB923C
- **Blanco**: #FFFFFF

## 📱 Diseño Responsivo

El sistema está optimizado para:
- Computadoras de escritorio
- Tablets
- Dispositivos móviles

## 🔍 Búsqueda Avanzada

El sistema incluye búsqueda en tiempo real en:
- Títulos de reuniones
- Descripciones de acuerdos
- Nombres de participantes
- Contenido de documentos

## 📈 Reportes y Estadísticas

- Reuniones por tipo y año
- Estado de acuerdos
- Participación por instituto
- Tendencias temporales

## 🔐 Seguridad

- Autenticación de usuarios
- Control de acceso por roles
- Validación de datos
- Protección CSRF

## 🚀 Despliegue en Producción

### Configuración de Producción

1. **Variables de Entorno**
```bash
export DEBUG=False
export SECRET_KEY='tu-clave-secreta'
export ALLOWED_HOSTS='tu-dominio.com'
```

2. **Base de Datos de Producción**
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'tecnm_reuniones_prod',
        'ENFORCE_SCHEMA': True,
        'CLIENT': {
            'host': 'tu-servidor-mongodb',
            'port': 27017,
            'username': 'usuario-prod',
            'password': 'contraseña-segura',
            'authSource': 'admin',
            'authMechanism': 'SCRAM-SHA-1'
        }
    }
}
```

3. **Archivos Estáticos**
```bash
python manage.py collectstatic
```

### Servidor Web

Recomendamos usar Gunicorn con Nginx:

```bash
pip install gunicorn
gunicorn mi_proyecto.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Solución de Problemas

### Error de Conexión a MongoDB
```bash
# Verificar que MongoDB esté ejecutándose
mongo --eval "db.runCommand('ping')"
```

### Error de Dependencias
```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### Error de Migraciones
```bash
# Limpiar migraciones
python manage.py migrate --fake-initial

# Crear nuevas migraciones
python manage.py makemigrations --empty mi_aplication
```

## 📞 Soporte

Para soporte técnico o reportar problemas:
- **Email**: soporte@tecnm.mx
- **Documentación**: [Enlace a documentación]
- **Issues**: [Enlace al repositorio de issues]

## 📄 Licencia

Este proyecto está desarrollado para el Tecnológico Nacional de México y está sujeto a las políticas institucionales.

## 🤝 Contribuciones

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Realiza tus cambios
4. Envía un Pull Request

## 📝 Changelog

### v1.0.0 (2024)
- Migración completa a MongoDB
- Sistema de reuniones nacionales
- Dashboard interactivo
- Gestión de acuerdos
- Sistema de participantes
- Documentos digitales
- Búsqueda avanzada
- Interfaz responsiva

---

**Desarrollado con ❤️ para la comunidad TecNM**
