from mongoengine import Document, StringField, DateTimeField, IntField, DecimalField, BooleanField, ReferenceField, ListField, EmbeddedDocumentField, EmbeddedDocument, URLField, EmailField
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

# Importar constantes centralizadas
from .constants import (
    TIPOS_DOCUMENTO, TIPOS_PARTICIPANTE, TIPOS_ACTIVIDAD, TIPOS_REUNION,
    ESTADOS_REUNION, MODALIDADES_REUNION, CATEGORIAS_ACUERDO, 
    ESTADOS_ACUERDO, PRIORIDADES, get_choice_display
)

# Modelos embebidos (nested objects)
class DocumentoEmbebido(EmbeddedDocument):
    """Documento embebido dentro de otros modelos"""
    titulo = StringField(required=True, max_length=200)
    descripcion = StringField()
    tipo = StringField(max_length=20, choices=TIPOS_DOCUMENTO)
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
    tipo_participante = StringField(max_length=20, choices=TIPOS_PARTICIPANTE)
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
    tipo_actividad = StringField(max_length=20, choices=TIPOS_ACTIVIDAD)
    documentos = ListField(EmbeddedDocumentField(DocumentoEmbebido))

# Modelos principales
class ReunionNacional(Document):
    """Modelo para las Reuniones Nacionales del TecNM"""
    
    # Usar constantes centralizadas
    TIPOS_REUNION = TIPOS_REUNION
    ESTADOS = ESTADOS_REUNION
    MODALIDADES = MODALIDADES_REUNION
    
    titulo = StringField(max_length=200, required=True)
    tipo = StringField(max_length=10, choices=TIPOS_REUNION, required=True)
    fecha_inicio = DateTimeField(required=True)
    fecha_fin = DateTimeField(required=True)
    sede = StringField(max_length=200, required=True)
    estado = StringField(max_length=15, choices=ESTADOS_REUNION, default='PLANIFICADA')
    modalidad = StringField(max_length=15, choices=MODALIDADES_REUNION, default='PRESENCIAL')
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
        return get_choice_display(TIPOS_REUNION, self.tipo)
    
    def get_estado_display(self):
        return get_choice_display(ESTADOS_REUNION, self.estado)
    
    def get_modalidad_display(self):
        return get_choice_display(MODALIDADES_REUNION, self.modalidad)
    
    def participantes_confirmados_count(self):
        return len([p for p in self.participantes if p.confirmado])
    
    def acuerdos_count(self):
        return Acuerdo.objects.filter(reunion=self).count()

class Acuerdo(Document):
    """Modelo para los acuerdos generados en las reuniones"""
    
    # Usar constantes centralizadas
    CATEGORIAS = CATEGORIAS_ACUERDO
    ESTADOS_ACUERDO = ESTADOS_ACUERDO
    PRIORIDADES = PRIORIDADES
    
    titulo = StringField(max_length=200, required=True)
    descripcion = StringField(required=True)
    categoria = StringField(max_length=20, choices=CATEGORIAS_ACUERDO, required=True)
    estado = StringField(max_length=20, choices=ESTADOS_ACUERDO, default='PENDIENTE')
    prioridad = StringField(max_length=10, choices=PRIORIDADES, default='MEDIA')
    
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
        return get_choice_display(CATEGORIAS_ACUERDO, self.categoria)
    
    def get_estado_display(self):
        return get_choice_display(ESTADOS_ACUERDO, self.estado)
    
    def get_prioridad_display(self):
        return get_choice_display(PRIORIDADES, self.prioridad)
    
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
    tipo_participante = StringField(max_length=20, choices=TIPOS_PARTICIPANTE)
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
        return get_choice_display(TIPOS_PARTICIPANTE, self.tipo_participante)

class Documento(Document):
    """Modelo independiente para documentos (cuando se necesita acceso directo)"""
    
    titulo = StringField(required=True, max_length=200)
    descripcion = StringField()
    tipo = StringField(max_length=20, choices=TIPOS_DOCUMENTO)
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
        return get_choice_display(TIPOS_DOCUMENTO, self.tipo)
