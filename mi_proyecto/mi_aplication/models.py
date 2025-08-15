from mongoengine import Document, StringField, DateTimeField, IntField, DecimalField, BooleanField, ReferenceField, ListField, EmbeddedDocumentField, EmbeddedDocument, URLField, EmailField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Modelos embebidos (nested objects)
class DocumentoEmbebido(EmbeddedDocument):
    """Documento embebido dentro de otros modelos"""
    titulo = StringField(required=True, max_length=200)
    descripcion = StringField()
    tipo = StringField(max_length=20, choices=[
        ('AGENDA', 'Agenda'),
        ('ACTA', 'Acta'),
        ('PRESENTACION', 'Presentación'),
        ('MEMORANDUM', 'Memorándum'),
        ('CIRCULAR', 'Circular'),
        ('OTRO', 'Otro'),
    ])
    url = URLField()
    formato = StringField(max_length=10)  # pdf, docx, pptx, etc.
    tamaño = IntField()  # en bytes
    version = StringField(default="1.0")
    fecha_subida = DateTimeField(default=timezone.now)
    subido_por = StringField(max_length=100)
    observaciones = StringField()

class ParticipanteEmbebido(EmbeddedDocument):
    """Participante embebido dentro de reuniones"""
    nombre = StringField(required=True, max_length=100)
    apellido_paterno = StringField(required=True, max_length=100)
    apellido_materno = StringField(max_length=100)
    email = EmailField(required=True)
    telefono = StringField(max_length=20)
    instituto = StringField(required=True, max_length=200)
    departamento = StringField(max_length=100)
    tipo_participante = StringField(max_length=20, choices=[
        ('DIRECTOR', 'Director'),
        ('SUBDIRECTOR', 'Subdirector'),
        ('COORDINADOR', 'Coordinador'),
        ('DOCENTE', 'Docente'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('INVITADO', 'Invitado'),
    ])
    confirmado = BooleanField(default=False)
    fecha_confirmacion = DateTimeField()
    observaciones = StringField()

class SeguimientoEmbebido(EmbeddedDocument):
    """Seguimiento embebido dentro de acuerdos"""
    fecha_seguimiento = DateTimeField(default=timezone.now)
    estado_anterior = StringField(max_length=20)
    estado_nuevo = StringField(max_length=20)
    porcentaje_avance = IntField(min_value=0, max_value=100)
    observaciones = StringField(required=True)
    responsable = StringField(max_length=100)
    documentos_relacionados = ListField(EmbeddedDocumentField(DocumentoEmbebido))

class AgendaEmbebido(EmbeddedDocument):
    """Agenda embebida dentro de reuniones"""
    titulo = StringField(required=True, max_length=200)
    descripcion = StringField()
    hora_inicio = StringField(max_length=10)  # formato HH:MM
    hora_fin = StringField(max_length=10)     # formato HH:MM
    responsable = StringField(max_length=100)
    tipo_actividad = StringField(max_length=20, choices=[
        ('PRESENTACION', 'Presentación'),
        ('DISCUSION', 'Discusión'),
        ('TRABAJO_GRUPO', 'Trabajo en Grupo'),
        ('RECESO', 'Receso'),
        ('OTRO', 'Otro'),
    ])
    documentos = ListField(EmbeddedDocumentField(DocumentoEmbebido))

# Modelos principales
class ReunionNacional(Document):
    """Modelo para las Reuniones Nacionales del TecNM"""
    
    TIPOS_REUNION = [
        ('RNSA', 'Reunión Nacional de Subdirectores Académicos'),
        ('RNPD', 'Reunión Nacional de Posgrado y Desarrollo'),
        ('RNVE', 'Reunión Nacional de Vinculación y Extensión'),
        ('RNCA', 'Reunión Nacional de Calidad y Acreditación'),
        ('OTRA', 'Otra Reunión Nacional'),
    ]
    
    ESTADOS = [
        ('PLANIFICADA', 'Planificada'),
        ('EN_CURSO', 'En Curso'),
        ('FINALIZADA', 'Finalizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    MODALIDADES = [
        ('PRESENCIAL', 'Presencial'),
        ('VIRTUAL', 'Virtual'),
        ('HIBRIDA', 'Híbrida'),
    ]
    
    titulo = StringField(max_length=200, required=True)
    tipo = StringField(max_length=10, choices=TIPOS_REUNION, required=True)
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField(required=True)
    sede = StringField(max_length=200, required=True)
    estado = StringField(max_length=15, choices=ESTADOS, default='PLANIFICADA')
    modalidad = StringField(max_length=15, choices=MODALIDADES, default='PRESENCIAL')
    enlace_videollamada = URLField(null=True, blank=True)
    direccion_fisica = StringField(max_length=500, null=True, blank=True)
    descripcion = StringField(required=True)
    objetivos = StringField(required=True)
    participantes_esperados = IntField(default=0)
    presupuesto_asignado = DecimalField(precision=2, null=True)
    organizador_principal = StringField(max_length=100, null=True)
    fecha_creacion = DateTimeField(default=timezone.now)
    fecha_actualizacion = DateTimeField(default=timezone.now)
    
    # Objetos anidados
    participantes = ListField(EmbeddedDocumentField(ParticipanteEmbebido))
    agenda = ListField(EmbeddedDocumentField(AgendaEmbebido))
    documentos = ListField(EmbeddedDocumentField(DocumentoEmbebido))
    
    meta = {
        'collection': 'reuniones_nacionales',
        'ordering': ['-fecha_inicio'],
        'indexes': ['tipo', 'estado', 'fecha_inicio']
    }
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()} ({self.fecha_inicio.strftime('%Y-%m-%d')})"
    
    def get_tipo_display(self):
        return dict(self.TIPOS_REUNION).get(self.tipo, self.tipo)
    
    def get_estado_display(self):
        return dict(self.ESTADOS).get(self.estado, self.estado)
    
    def get_modalidad_display(self):
        return dict(self.MODALIDADES).get(self.modalidad, self.modalidad)
    
    def participantes_confirmados_count(self):
        return len([p for p in self.participantes if p.confirmado])
    
    def acuerdos_count(self):
        return Acuerdo.objects.filter(reunion=self).count()

class Acuerdo(Document):
    """Modelo para los Acuerdos de las Reuniones Nacionales"""
    
    CATEGORIAS = [
        ('ACADEMICA', 'Académica'),
        ('ADMINISTRATIVA', 'Administrativa'),
        ('FINANCIERA', 'Financiera'),
        ('INFRAESTRUCTURA', 'Infraestructura'),
        ('VINCULACION', 'Vinculación'),
        ('INVESTIGACION', 'Investigación'),
        ('OTRA', 'Otra'),
    ]
    
    ESTADOS_ACUERDO = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
        ('SUSPENDIDO', 'Suspendido'),
    ]
    
    titulo = StringField(max_length=200, required=True)
    descripcion = StringField(required=True)
    categoria = StringField(max_length=20, choices=CATEGORIAS, required=True)
    estado = StringField(max_length=20, choices=ESTADOS_ACUERDO, default='PENDIENTE')
    prioridad = StringField(max_length=10, choices=[
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ], default='MEDIA')
    
    # Referencias
    reunion = ReferenceField(ReunionNacional, required=True)
    
    # Campos de seguimiento
    responsable = StringField(max_length=100, required=True)
    fecha_limite = DateTimeField()
    fecha_creacion = DateTimeField(default=timezone.now)
    fecha_actualizacion = DateTimeField(default=timezone.now)
    
    # Objetos anidados
    seguimientos = ListField(EmbeddedDocumentField(SeguimientoEmbebido))
    documentos = ListField(EmbeddedDocumentField(DocumentoEmbebido))
    
    meta = {
        'collection': 'acuerdos',
        'ordering': ['-fecha_creacion'],
        'indexes': ['reunion', 'categoria', 'estado', 'responsable']
    }
    
    def __str__(self):
        return f"{self.titulo} - {self.get_categoria_display()}"
    
    def get_categoria_display(self):
        return dict(self.CATEGORIAS).get(self.categoria, self.categoria)
    
    def get_estado_display(self):
        return dict(self.ESTADOS_ACUERDO).get(self.estado, self.estado)
    
    def get_prioridad_display(self):
        return dict([
            ('BAJA', 'Baja'),
            ('MEDIA', 'Media'),
            ('ALTA', 'Alta'),
            ('CRITICA', 'Crítica'),
        ]).get(self.prioridad, self.prioridad)
    
    def ultimo_seguimiento(self):
        if self.seguimientos:
            return max(self.seguimientos, key=lambda x: x.fecha_seguimiento)
        return None

# Modelos independientes para casos especiales
class Participante(Document):
    """Modelo independiente para participantes (cuando se necesita acceso directo)"""
    
    nombre = StringField(required=True, max_length=100)
    apellido_paterno = StringField(required=True, max_length=100)
    apellido_materno = StringField(max_length=100)
    email = EmailField(required=True, unique=True)
    telefono = StringField(max_length=20)
    instituto = StringField(required=True, max_length=200)
    departamento = StringField(max_length=100)
    tipo_participante = StringField(max_length=20, choices=[
        ('DIRECTOR', 'Director'),
        ('SUBDIRECTOR', 'Subdirector'),
        ('COORDINADOR', 'Coordinador'),
        ('DOCENTE', 'Docente'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('INVITADO', 'Invitado'),
    ])
    confirmado = BooleanField(default=False)
    fecha_confirmacion = DateTimeField()
    observaciones = StringField()
    
    # Referencias
    reuniones = ListField(ReferenceField(ReunionNacional))
    
    meta = {
        'collection': 'participantes',
        'ordering': ['apellido_paterno', 'nombre'],
        'indexes': ['email', 'instituto', 'tipo_participante']
    }
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    def get_tipo_participante_display(self):
        return dict([
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('INVITADO', 'Invitado'),
        ]).get(self.tipo_participante, self.tipo_participante)

class Documento(Document):
    """Modelo independiente para documentos (cuando se necesita acceso directo)"""
    
    titulo = StringField(required=True, max_length=200)
    descripcion = StringField()
    tipo = StringField(max_length=20, choices=[
        ('AGENDA', 'Agenda'),
        ('ACTA', 'Acta'),
        ('PRESENTACION', 'Presentación'),
        ('MEMORANDUM', 'Memorándum'),
        ('CIRCULAR', 'Circular'),
        ('OTRO', 'Otro'),
    ])
    url = URLField()
    formato = StringField(max_length=10)
    tamaño = IntField()
    version = StringField(default="1.0")
    fecha_subida = DateTimeField(default=timezone.now)
    subido_por = StringField(max_length=100)
    observaciones = StringField()
    
    # Referencias
    reunion = ReferenceField(ReunionNacional, null=True)
    acuerdo = ReferenceField(Acuerdo, null=True)
    
    meta = {
        'collection': 'documentos',
        'ordering': ['-fecha_subida'],
        'indexes': ['tipo', 'formato', 'reunion', 'acuerdo']
    }
    
    def __str__(self):
        return f"{self.titulo} - {self.get_tipo_display()}"
    
    def get_tipo_display(self):
        return dict([
            ('AGENDA', 'Agenda'),
            ('ACTA', 'Acta'),
            ('PRESENTACION', 'Presentación'),
            ('MEMORANDUM', 'Memorándum'),
            ('CIRCULAR', 'Circular'),
            ('OTRO', 'Otro'),
        ]).get(self.tipo, self.tipo)
