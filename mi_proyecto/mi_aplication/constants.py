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
    ('CURSO_CAPACITACION', 'Curso de Capacitación'),
    ('TALLER', 'Taller'),
    ('SEMINARIO', 'Seminario'),
    ('CONFERENCIA', 'Conferencia'),
    ('DIPLOMADO', 'Diplomado'),
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
    ('CONSTANCIA', 'Constancia'),
    ('CERTIFICADO', 'Certificado'),
    ('DIPLOMA', 'Diploma'),
    ('OTRO', 'Otro'),
]

# ===== OPCIONES DE SEXO =====
SEXOS = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ('N', 'No especifica'),
]

# ===== ÁREAS DEPARTAMENTALES =====
AREAS_DEPARTAMENTO = [
    ('SISTEMAS_COMPUTACIONALES', 'Sistemas Computacionales'),
    ('INDUSTRIAL', 'Ingeniería Industrial'),
    ('ELECTRONICA', 'Ingeniería Electrónica'),
    ('MECANICA', 'Ingeniería Mecánica'),
    ('CIVIL', 'Ingeniería Civil'),
    ('QUIMICA', 'Ingeniería Química'),
    ('ELECTRICA', 'Ingeniería Eléctrica'),
    ('GESTION_EMPRESARIAL', 'Gestión Empresarial'),
    ('CONTADOR_PUBLICO', 'Contador Público'),
    ('ADMINISTRACION', 'Administración'),
    ('MATEMATICAS', 'Matemáticas y Ciencias Básicas'),
    ('HUMANIDADES', 'Humanidades y Ciencias Sociales'),
    ('INVESTIGACION', 'Investigación y Posgrado'),
    ('VINCULACION', 'Vinculación'),
    ('PLANEACION', 'Planeación y Evaluación'),
    ('RECURSOS_HUMANOS', 'Recursos Humanos'),
    ('FINANZAS', 'Recursos Financieros'),
    ('MATERIALES', 'Recursos Materiales'),
    ('SERVICIOS_ESCOLARES', 'Servicios Escolares'),
    ('BIBLIOTECA', 'Biblioteca'),
    ('COMPUTO', 'Centro de Cómputo'),
    ('MANTENIMIENTO', 'Mantenimiento'),
    ('DIRECCION', 'Dirección'),
    ('SUBDIRECCION_ACADEMICA', 'Subdirección Académica'),
    ('SUBDIRECCION_PLANEACION', 'Subdirección de Planeación'),
    ('OTRA', 'Otra Área'),
]

# ===== CATEGORÍAS FORMATIVAS =====
CATEGORIAS_FORMATIVAS = [
    ('DOCENTE_TECNM', 'Docente TecNM'),
    ('MATEMATICAS_CIENCIAS', 'Matemáticas y Ciencias Básicas'),
    ('FORMACION_DISCIPLINAR', 'Formación Disciplinar'),
    ('PSICOPEDAGOGIA_E_INVESTIGACION', 'Psicopedagogía e Investigación'),
    ('TECNOLOGIAS_DIGITALES','Tecnologías Digitales'),
    ('EMPRENDIMIENTO_FINANZAS', 'Emprendimiento y Finanzas'),
    ('GESTION_LIDERAZGO', 'Gestión y Liderazgo'),
]

# ===== CURSOS ESPECÍFICOS =====
CURSOS_ESPECIFICOS = [
    # Tecnología e Innovación
    ('CIENCIA_DATOS', 'Ciencia de Datos'),
    ('INTELIGENCIA_ARTIFICIAL', 'Inteligencia Artificial'),
    ('DESARROLLO_DE_APLICACIONES', 'Desarrollo de Aplicaciones'),
    ('CIBERSEGURIDAD', 'Ciberseguridad'),
    
    # Educación y Pedagogía
    ('PEDAGOGIA_DIGITAL', 'Pedagogía Digital'),
    ('EVALUACION_EDUCATIVA', 'Evaluación Educativa'),
    ('DISEÑO_CURRICULAR', 'Diseño Curricular'),
    ('COMPETENCIAS_DIGITALES', 'Competencias Digitales'),
    ('METODOLOGIAS_ACTIVAS', 'Metodologías Activas de Aprendizaje'),
    ('EDUCACION_VIRTUAL', 'Educación Virtual'),
    
    # Gestión y Administración
    ('LIDERAZGO', 'Liderazgo'),
    ('GESTION_PROYECTOS', 'Gestión de Proyectos'),
    ('ADMINISTRACION_PUBLICA', 'Administración Pública'),
    ('FINANZAS_PUBLICAS', 'Finanzas Públicas'),
    ('RECURSOS_HUMANOS', 'Gestión de Recursos Humanos'),
    ('CALIDAD_EDUCATIVA', 'Calidad Educativa'),
    ('PLANEACION_ESTRATEGICA', 'Planeación Estratégica'),
    
    # Investigación
    ('METODOLOGIA_INVESTIGACION', 'Metodología de la Investigación'),
    ('ESTADISTICA_AVANZADA', 'Estadística Avanzada'),
    ('REDACCION_CIENTIFICA', 'Redacción Científica'),
    ('PROPIEDAD_INTELECTUAL', 'Propiedad Intelectual'),
    
    # Idiomas
    ('INGLES_TECNICO', 'Inglés Técnico'),
    ('FRANCES', 'Francés'),
    ('ALEMAN', 'Alemán'),
    
    # Otros
    ('SUSTENTABILIDAD', 'Sustentabilidad'),
    ('EMPRENDIMIENTO', 'Emprendimiento'),
    ('INNOVACION_EDUCATIVA', 'Innovación Educativa'),
    ('VINCULACION_EMPRESA', 'Vinculación con la Empresa'),
    ('OTRO', 'Otro Curso'),
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

# ===== CATÁLOGO DE PLANTELES TECNM =====
PLANTELES_TECNM = [
    # Región Noroeste
    ('ITT_TIJUANA', 'Instituto Tecnológico de Tijuana'),
    ('ITT_MEXICALI', 'Instituto Tecnológico de Mexicali'),
    ('ITT_ENSENADA', 'Instituto Tecnológico de Ensenada'),
    ('ITT_LA_PAZ', 'Instituto Tecnológico de La Paz'),
    ('ITT_LOS_CABOS', 'Instituto Tecnológico de Los Cabos'),
    ('ITT_HERMOSILLO', 'Instituto Tecnológico de Hermosillo'),
    ('ITT_NOGALES', 'Instituto Tecnológico de Nogales'),
    ('ITT_CIUDAD_OBREGON', 'Instituto Tecnológico de Ciudad Obregón'),
    ('ITT_GUAYMAS', 'Instituto Tecnológico de Guaymas'),
    ('ITT_CULIACAN', 'Instituto Tecnológico de Culiacán'),
    ('ITT_MAZATLAN', 'Instituto Tecnológico de Mazatlán'),
    ('ITT_LOS_MOCHIS', 'Instituto Tecnológico de Los Mochis'),
    
    # Región Norte
    ('ITT_CHIHUAHUA', 'Instituto Tecnológico de Chihuahua'),
    ('ITT_CIUDAD_JUAREZ', 'Instituto Tecnológico de Ciudad Juárez'),
    ('ITT_DELICIAS', 'Instituto Tecnológico de Delicias'),
    ('ITT_PARRAL', 'Instituto Tecnológico de Parral'),
    ('ITT_DURANGO', 'Instituto Tecnológico de Durango'),
    ('ITT_GOMEZ_PALACIO', 'Instituto Tecnológico de Gómez Palacio'),
    ('ITT_TORREON', 'Instituto Tecnológico de Torreón'),
    ('ITT_SALTILLO', 'Instituto Tecnológico de Saltillo'),
    ('ITT_MONCLOVA', 'Instituto Tecnológico de Monclova'),
    ('ITT_PIEDRAS_NEGRAS', 'Instituto Tecnológico de Piedras Negras'),
    
    # Región Noreste
    ('ITT_MONTERREY', 'Instituto Tecnológico de Monterrey Campus TecNM'),
    ('ITT_NUEVO_LAREDO', 'Instituto Tecnológico de Nuevo Laredo'),
    ('ITT_REYNOSA', 'Instituto Tecnológico de Reynosa'),
    ('ITT_MATAMOROS', 'Instituto Tecnológico de Matamoros'),
    ('ITT_CIUDAD_VICTORIA', 'Instituto Tecnológico de Ciudad Victoria'),
    ('ITT_TAMPICO', 'Instituto Tecnológico de Tampico'),
    ('ITT_MADERO', 'Instituto Tecnológico de Cd. Madero'),
    
    # Región Occidente
    ('ITT_GUADALAJARA', 'Instituto Tecnológico de Guadalajara'),
    ('ITT_ZAPOPAN', 'Instituto Tecnológico de Zapopan'),
    ('ITT_PUERTO_VALLARTA', 'Instituto Tecnológico de Puerto Vallarta'),
    ('ITT_COLIMA', 'Instituto Tecnológico de Colima'),
    ('ITT_MANZANILLO', 'Instituto Tecnológico de Manzanillo'),
    ('ITT_AGUASCALIENTES', 'Instituto Tecnológico de Aguascalientes'),
    ('ITT_ZACATECAS', 'Instituto Tecnológico de Zacatecas'),
    ('ITT_FRESNILLO', 'Instituto Tecnológico de Fresnillo'),
    
    # Región Centro Occidente
    ('ITT_MORELIA', 'Instituto Tecnológico de Morelia'),
    ('ITT_URUAPAN', 'Instituto Tecnológico de Uruapan'),
    ('ITT_LAZARO_CARDENAS', 'Instituto Tecnológico de Lázaro Cárdenas'),
    ('ITT_LEON', 'Instituto Tecnológico de León'),
    ('ITT_CELAYA', 'Instituto Tecnológico de Celaya'),
    ('ITT_IRAPUATO', 'Instituto Tecnológico de Irapuato'),
    ('ITT_SAN_LUIS_POTOSI', 'Instituto Tecnológico de San Luis Potosí'),
    
    # Región Centro
    ('ITT_TOLUCA', 'Instituto Tecnológico de Toluca'),
    ('ITT_PACHUCA', 'Instituto Tecnológico de Pachuca'),
    ('ITT_TULA_TEPEJI', 'Instituto Tecnológico de Tula-Tepeji'),
    ('ITT_QUERETARO', 'Instituto Tecnológico de Querétaro'),
    ('ITT_TLALNEPANTLA', 'Instituto Tecnológico de Tlalnepantla'),
    ('ITT_VALLE_MEXICO', 'Instituto Tecnológico del Valle de México'),
    
    # Región Oriente
    ('ITT_PUEBLA', 'Instituto Tecnológico de Puebla'),
    ('ITT_TEHUACAN', 'Instituto Tecnológico de Tehuacán'),
    ('ITT_VERACRUZ', 'Instituto Tecnológico de Veracruz'),
    ('ITT_XALAPA', 'Instituto Tecnológico de Xalapa'),
    ('ITT_ORIZABA', 'Instituto Tecnológico de Orizaba'),
    ('ITT_MINATITLAN', 'Instituto Tecnológico de Minatitlán'),
    ('ITT_TLAXLA', 'Instituto Tecnológico de Tlaxcala'),
    
    # Región Sur Sureste
    ('ITT_OAXACA', 'Instituto Tecnológico de Oaxaca'),
    ('ITT_TUXTLA_GUTIERREZ', 'Instituto Tecnológico de Tuxtla Gutiérrez'),
    ('ITT_TAPACHULA', 'Instituto Tecnológico de Tapachula'),
    ('ITT_VILLAHERMOSA', 'Instituto Tecnológico de Villahermosa'),
    ('ITT_MERIDA', 'Instituto Tecnológico de Mérida'),
    ('ITT_CAMPECHE', 'Instituto Tecnológico de Campeche'),
    ('ITT_CHETUMAL', 'Instituto Tecnológico de Chetumal'),
    ('ITT_CANCUN', 'Instituto Tecnológico de Cancún'),
    
    # Universidades Tecnológicas
    ('UTT_HERMOSILLO', 'Universidad Tecnológica de Hermosillo'),
    ('UTT_TIJUANA', 'Universidad Tecnológica de Tijuana'),
    ('UTT_PUEBLA', 'Universidad Tecnológica de Puebla'),
    ('UTT_NEZAHUALCOYOTL', 'Universidad Tecnológica de Nezahualcóyotl'),
    
    # Institutos Tecnológicos Descentralizados
    ('ITD_CHIHUAHUA_II', 'Instituto Tecnológico de Chihuahua II'),
    ('ITD_ESTUDIOS_SUPERIORES_MONTERREY', 'Instituto Tecnológico de Estudios Superiores de Monterrey'),
    
    # Oficinas Centrales
    ('TECNM_OFICINAS_CENTRALES', 'TecNM - Oficinas Centrales'),
    ('OTRO_PLANTEL', 'Otro Plantel'),
]

# ===== ROLES DEL SISTEMA =====
ROLES_USUARIO = [
    ('PARTICIPANTE', 'Participante'),
    ('EDITOR', 'Editor'),
    ('ADMIN', 'Administrador'),
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