"""
Constantes centralizadas para el Sistema de Reuniones Nacionales TecNM

Este módulo contiene todas las constantes, choices y configuraciones
utilizadas en todo el sistema para evitar duplicación y facilitar
el mantenimiento.
"""

# ===== TIPOS DE REUNIÓN =====
TIPOS_REUNION = [
    ('RNSA', 'Reunión Nacional de Subdirectores Académicos'),
    ('RNPD', 'Reunión Nacional de Posgrado y Desarrollo'),
    ('RNVE', 'Reunión Nacional de Vinculación y Extensión'),
    ('RNCA', 'Reunión Nacional de Calidad y Acreditación'),
    ('RNTI', 'Reunión Nacional de Tecnologías de la Información'),
    ('RNRH', 'Reunión Nacional de Recursos Humanos'),
    ('RNAF', 'Reunión Nacional de Administración y Finanzas'),
    ('OTRA', 'Otra Reunión Nacional'),
]

# ===== ESTADOS DE REUNIÓN =====
ESTADOS_REUNION = [
    ('PLANIFICADA', 'Planificada'),
    ('EN_CURSO', 'En Curso'),
    ('FINALIZADA', 'Finalizada'),
    ('CANCELADA', 'Cancelada'),
    ('SUSPENDIDA', 'Suspendida'),
]

# ===== MODALIDADES DE REUNIÓN =====
MODALIDADES_REUNION = [
    ('PRESENCIAL', 'Presencial'),
    ('VIRTUAL', 'Virtual'),
    ('HIBRIDA', 'Híbrida'),
]

# ===== TIPOS DE PARTICIPANTE =====
TIPOS_PARTICIPANTE = [
    ('DIRECTOR', 'Director'),
    ('SUBDIRECTOR', 'Subdirector'),
    ('COORDINADOR', 'Coordinador'),
    ('DOCENTE', 'Docente'),
    ('ADMINISTRATIVO', 'Administrativo'),
    ('DOCENTE_TECNM', 'Docente TecNM'),
    ('MATEMATICAS_CIENCIAS', 'Matemáticas y Ciencias Básicas'),
    ('JEFE_DEPARTAMENTO', 'Jefe de Departamento'),
    ('INVESTIGADOR', 'Investigador'),
    ('INVITADO', 'Invitado'),
    ('ESTUDIANTE', 'Estudiante'),
    ('EXTERNO', 'Externo'),
]

# ===== CATEGORÍAS DE ACUERDO =====
CATEGORIAS_ACUERDO = [
    ('ACADEMICA', 'Académica'),
    ('ADMINISTRATIVA', 'Administrativa'),
    ('FINANCIERA', 'Financiera'),
    ('INFRAESTRUCTURA', 'Infraestructura'),
    ('RECURSOS_HUMANOS', 'Recursos Humanos'),
    ('TECNOLOGICA', 'Tecnológica'),
    ('VINCULACION', 'Vinculación'),
    ('INVESTIGACION', 'Investigación'),
    ('CALIDAD', 'Calidad y Acreditación'),
    ('NORMATIVA', 'Normativa'),
    ('OTRA', 'Otra'),
]

# ===== ESTADOS DE ACUERDO =====
ESTADOS_ACUERDO = [
    ('PENDIENTE', 'Pendiente'),
    ('EN_PROCESO', 'En Proceso'),
    ('COMPLETADO', 'Completado'),
    ('CANCELADO', 'Cancelado'),
    ('SUSPENDIDO', 'Suspendido'),
    ('VENCIDO', 'Vencido'),
]

# ===== PRIORIDADES =====
PRIORIDADES = [
    ('BAJA', 'Baja'),
    ('MEDIA', 'Media'),
    ('ALTA', 'Alta'),
    ('CRITICA', 'Crítica'),
    ('URGENTE', 'Urgente'),
]

# ===== TIPOS DE DOCUMENTO =====
TIPOS_DOCUMENTO = [
    ('AGENDA', 'Agenda'),
    ('ACTA', 'Acta'),
    ('PRESENTACION', 'Presentación'),
    ('MEMORANDUM', 'Memorándum'),
    ('CIRCULAR', 'Circular'),
    ('MANUAL', 'Manual'),
    ('REPORTE', 'Reporte'),
    ('INFORME', 'Informe'),
    ('PROPUESTA', 'Propuesta'),
    ('CONVENIO', 'Convenio'),
    ('CONTRATO', 'Contrato'),
    ('ESTADISTICAS', 'Estadísticas'),
    ('NORMATIVA', 'Normativa'),
    ('OTRO', 'Otro'),
]

# ===== FORMATOS DE ARCHIVO =====
FORMATOS_ARCHIVO = [
    ('pdf', 'PDF'),
    ('docx', 'Word Document'),
    ('pptx', 'PowerPoint'),
    ('xlsx', 'Excel'),
    ('txt', 'Texto Plano'),
    ('jpg', 'Imagen JPEG'),
    ('png', 'Imagen PNG'),
    ('zip', 'Archivo Comprimido'),
    ('otro', 'Otro'),
]

# ===== TIPOS DE ACTIVIDAD EN AGENDA =====
TIPOS_ACTIVIDAD = [
    ('PRESENTACION', 'Presentación'),
    ('DISCUSION', 'Discusión'),
    ('TRABAJO_GRUPO', 'Trabajo en Grupo'),
    ('MESA_REDONDA', 'Mesa Redonda'),
    ('CONFERENCIA', 'Conferencia Magistral'),
    ('TALLER', 'Taller'),
    ('CEREMONIA', 'Ceremonia'),
    ('RECESO', 'Receso'),
    ('COMIDA', 'Comida'),
    ('NETWORKING', 'Networking'),
    ('OTRO', 'Otro'),
]

# ===== INSTITUTOS TECNM (ALGUNOS EJEMPLOS) =====
INSTITUTOS_TECNM = [
    ('ITA', 'Instituto Tecnológico de Aguascalientes'),
    ('ITCM', 'Instituto Tecnológico de Ciudad Madero'),
    ('ITESM', 'Instituto Tecnológico de Estudios Superiores de Monterrey'),
    ('ITM', 'Instituto Tecnológico de Mérida'),
    ('ITMORELIA', 'Instituto Tecnológico de Morelia'),
    ('ITPUEBLA', 'Instituto Tecnológico de Puebla'),
    ('ITQUERETARO', 'Instituto Tecnológico de Querétaro'),
    ('ITTOLUCA', 'Instituto Tecnológico de Toluca'),
    ('ITVERACRUZ', 'Instituto Tecnológico de Veracruz'),
    ('OTRO', 'Otro Instituto'),
]

# ===== DEPARTAMENTOS ACADÉMICOS =====
DEPARTAMENTOS_ACADEMICOS = [
    ('SISTEMAS', 'Sistemas Computacionales'),
    ('ELECTRONICA', 'Ingeniería Electrónica'),
    ('INDUSTRIAL', 'Ingeniería Industrial'),
    ('CIVIL', 'Ingeniería Civil'),
    ('MECANICA', 'Ingeniería Mecánica'),
    ('QUIMICA', 'Ingeniería Química'),
    ('MATEMATICAS', 'Matemáticas y Ciencias Básicas'),
    ('DESARROLLO_ACADEMICO', 'Desarrollo Académico'),
    ('INVESTIGACION', 'Investigación y Posgrado'),
    ('VINCULACION', 'Vinculación y Extensión'),
    ('RECURSOS_HUMANOS', 'Recursos Humanos'),
    ('ADMINISTRACION', 'Administración y Finanzas'),
    ('DIRECCION', 'Dirección'),
    ('OTRO', 'Otro Departamento'),
]

# ===== CONFIGURACIONES DEL SISTEMA =====
CONFIGURACIONES_SISTEMA = {
    'MAX_PARTICIPANTES_POR_REUNION': 1000,
    'MAX_DOCUMENTOS_POR_REUNION': 50,
    'MAX_ACUERDOS_POR_REUNION': 100,
    'TAMAÑO_MAXIMO_ARCHIVO_MB': 100,
    'DIAS_RECORDATORIO_REUNION': 7,
    'HORAS_EDICION_ACTA': 48,
}

# ===== FUNCIONES DE UTILIDAD =====

def get_choice_display(choices_list, value):
    """
    Obtiene el display name de un valor en una lista de choices
    
    Args:
        choices_list: Lista de tuplas (value, display)
        value: Valor a buscar
        
    Returns:
        str: Display name del valor o el valor original si no se encuentra
    """
    choices_dict = dict(choices_list)
    return choices_dict.get(value, value)

def get_choices_dict(choices_list):
    """
    Convierte una lista de choices en diccionario
    
    Args:
        choices_list: Lista de tuplas (value, display)
        
    Returns:
        dict: Diccionario con values como keys y displays como values
    """
    return dict(choices_list)

def get_all_choice_values(choices_list):
    """
    Obtiene todos los valores de una lista de choices
    
    Args:
        choices_list: Lista de tuplas (value, display)
        
    Returns:
        list: Lista de valores
    """
    return [choice[0] for choice in choices_list]

def get_all_choice_displays(choices_list):
    """
    Obtiene todos los displays de una lista de choices
    
    Args:
        choices_list: Lista de tuplas (value, display)
        
    Returns:
        list: Lista de displays
    """
    return [choice[1] for choice in choices_list]

# ===== VALIDACIONES DE CHOICES =====

def validate_choice(value, choices_list, field_name="campo"):
    """
    Valida que un valor esté en la lista de choices permitidos
    
    Args:
        value: Valor a validar
        choices_list: Lista de choices válidos
        field_name: Nombre del campo para error
        
    Returns:
        str or None: Mensaje de error o None si es válido
    """
    valid_values = get_all_choice_values(choices_list)
    if value and value not in valid_values:
        valid_displays = ', '.join(get_all_choice_displays(choices_list))
        return f"El valor '{value}' no es válido para {field_name}. Valores válidos: {valid_displays}"
    return None

# ===== CONFIGURACIONES POR DEFECTO =====

DEFAULTS = {
    'TIPO_REUNION': 'OTRA',
    'ESTADO_REUNION': 'PLANIFICADA',
    'MODALIDAD_REUNION': 'PRESENCIAL',
    'TIPO_PARTICIPANTE': 'INVITADO',
    'CATEGORIA_ACUERDO': 'OTRA',
    'ESTADO_ACUERDO': 'PENDIENTE',
    'PRIORIDAD': 'MEDIA',
    'TIPO_DOCUMENTO': 'OTRO',
    'FORMATO_ARCHIVO': 'pdf',
    'TIPO_ACTIVIDAD': 'OTRO',
}

# ===== MAPEOS PARA MIGRACIÓN =====
# En caso de que necesites mapear valores antiguos a nuevos

MAPEO_TIPOS_PARTICIPANTE_LEGACY = {
    'Docente TecNM': 'DOCENTE_TECNM',
    'Matemáticas y Ciencias Básicas': 'MATEMATICAS_CIENCIAS',
}

def migrar_tipo_participante(valor_legacy):
    """
    Migra valores legacy de tipo participante a los nuevos valores
    """
    return MAPEO_TIPOS_PARTICIPANTE_LEGACY.get(valor_legacy, valor_legacy)