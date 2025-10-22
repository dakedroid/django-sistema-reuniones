from datetime import datetime, date
from bson import ObjectId
from django.core.exceptions import ValidationError
from django.utils import timezone
import re

def validar_fechas_reunion(fecha_inicio, fecha_fin):
    """Valida que las fechas de reunión sean consistentes"""
    errores = []
    
    if fecha_inicio and fecha_fin:
        if fecha_inicio >= fecha_fin:
            errores.append("La fecha de inicio debe ser anterior a la fecha de fin.")
        
        # Validar que no sean fechas muy en el pasado (más de 2 años)
        hace_dos_anos = timezone.now() - timezone.timedelta(days=730)
        if fecha_inicio < hace_dos_anos:
            errores.append("La fecha de inicio no puede ser de hace más de 2 años.")
    
    return errores

def validar_email_formato(email):
    """Valida que el email tenga formato correcto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return "El formato del email no es válido."
    return None

def validar_telefono(telefono):
    """Valida que el teléfono tenga formato correcto"""
    if telefono:
        # Permitir números con espacios, guiones, paréntesis
        pattern = r'^[\d\s\-\(\)\+]{10,15}$'
        if not re.match(pattern, telefono.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")):
            return "El formato del teléfono no es válido. Debe tener entre 10 y 15 dígitos."
    return None

def validar_url(url):
    """Valida que la URL tenga formato correcto"""
    if url:
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
        if not re.match(pattern, url):
            return "El formato de la URL no es válido."
    return None

def validar_tamaño_archivo(tamaño):
    """Valida que el tamaño del archivo sea razonable"""
    if tamaño:
        try:
            tamaño_int = int(tamaño)
            if tamaño_int < 0:
                return "El tamaño del archivo no puede ser negativo."
            if tamaño_int > 100000000:  # 100 MB
                return "El tamaño del archivo no puede ser mayor a 100 MB."
        except ValueError:
            return "El tamaño del archivo debe ser un número."
    return None

def validar_presupuesto(presupuesto):
    """Valida que el presupuesto sea un valor positivo"""
    if presupuesto:
        try:
            presupuesto_float = float(presupuesto)
            if presupuesto_float < 0:
                return "El presupuesto no puede ser negativo."
            if presupuesto_float > 10000000:  # 10 millones
                return "El presupuesto no puede ser mayor a $10,000,000."
        except ValueError:
            return "El presupuesto debe ser un número válido."
    return None

def validar_participantes_esperados(participantes_esperados):
    """Valida que el número de participantes esperados sea razonable"""
    if participantes_esperados:
        try:
            participantes_int = int(participantes_esperados)
            if participantes_int < 1:
                return "Debe esperarse al menos 1 participante."
            if participantes_int > 1000:
                return "El número de participantes esperados no puede ser mayor a 1000."
        except ValueError:
            return "El número de participantes esperados debe ser un número entero."
    return None

def validar_duplicado_email_participante(email, participante_id=None):
    """Valida que no haya emails duplicados en participantes"""
    from .models import Participante
    
    try:
        query = Participante.objects.filter(email=email)
        if participante_id:
            query = query.filter(id__ne=ObjectId(participante_id))
        
        if query.count() > 0:
            return "Ya existe un participante con este email."
    except Exception:
        pass
    
    return None

def limpiar_y_validar_texto(texto, campo_nombre, max_length=None, required=True):
    """Limpia y valida campos de texto"""
    errores = []
    
    if texto:
        texto = texto.strip()
    
    if required and (not texto or texto == ""):
        errores.append(f"El campo {campo_nombre} es obligatorio.")
    
    if texto and max_length and len(texto) > max_length:
        errores.append(f"El campo {campo_nombre} no puede tener más de {max_length} caracteres.")
    
    # Validar caracteres especiales peligrosos
    if texto:
        caracteres_peligrosos = ['<', '>', '"', "'", '&']
        for caracter in caracteres_peligrosos:
            if caracter in texto:
                errores.append(f"El campo {campo_nombre} contiene caracteres no permitidos.")
                break
    
    return texto, errores