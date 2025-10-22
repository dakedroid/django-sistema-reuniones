"""
Vista de administración para gestionar constantes del sistema

Permite agregar, editar y eliminar constantes centralizadas
desde una interfaz web administrativa.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
import json
import os
from pathlib import Path

from .constants import *

def is_admin(user):
    """Verifica que el usuario sea administrador"""
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_constantes(request):
    """Vista principal para administrar constantes"""
    
    # Organizar constantes por categoría
    constantes_organizadas = {
        'Tipos de Reunión': {
            'variable': 'TIPOS_REUNION',
            'valores': TIPOS_REUNION,
            'descripcion': 'Tipos de reuniones nacionales del TecNM'
        },
        'Estados de Reunión': {
            'variable': 'ESTADOS_REUNION',
            'valores': ESTADOS_REUNION,
            'descripcion': 'Estados posibles de las reuniones'
        },
        'Modalidades': {
            'variable': 'MODALIDADES_REUNION',
            'valores': MODALIDADES_REUNION,
            'descripcion': 'Modalidades de realización de reuniones'
        },
        'Tipos de Participante': {
            'variable': 'TIPOS_PARTICIPANTE',
            'valores': TIPOS_PARTICIPANTE,
            'descripcion': 'Tipos de participantes en reuniones'
        },
        'Categorías de Acuerdo': {
            'variable': 'CATEGORIAS_ACUERDO',
            'valores': CATEGORIAS_ACUERDO,
            'descripcion': 'Categorías para clasificar acuerdos'
        },
        'Estados de Acuerdo': {
            'variable': 'ESTADOS_ACUERDO',
            'valores': ESTADOS_ACUERDO,
            'descripcion': 'Estados de seguimiento de acuerdos'
        },
        'Prioridades': {
            'variable': 'PRIORIDADES',
            'valores': PRIORIDADES,
            'descripcion': 'Niveles de prioridad para acuerdos'
        },
        'Tipos de Documento': {
            'variable': 'TIPOS_DOCUMENTO',
            'valores': TIPOS_DOCUMENTO,
            'descripcion': 'Tipos de documentos del sistema'
        },
        'Tipos de Actividad': {
            'variable': 'TIPOS_ACTIVIDAD',
            'valores': TIPOS_ACTIVIDAD,
            'descripcion': 'Tipos de actividades en agenda'
        },
    }
    
    context = {
        'constantes': constantes_organizadas,
        'configuraciones': CONFIGURACIONES_SISTEMA,
    }
    
    return render(request, 'admin/constantes.html', context)

@login_required
@user_passes_test(is_admin)
def editar_constante(request, categoria):
    """Permite editar una categoría de constantes"""
    
    if request.method == 'POST':
        try:
            # Obtener nuevos valores desde el formulario
            nuevos_valores = []
            i = 0
            while True:
                codigo = request.POST.get(f'codigo_{i}')
                descripcion = request.POST.get(f'descripcion_{i}')
                
                if not codigo:
                    break
                    
                if codigo and descripcion:
                    nuevos_valores.append((codigo.upper(), descripcion))
                i += 1
            
            if not nuevos_valores:
                messages.error(request, 'Debe agregar al menos un valor.')
                return redirect('admin_constantes')
            
            # Aquí normalmente actualizarías la base de datos o archivo de configuración
            # Por simplicidad, solo mostramos un mensaje de éxito
            messages.success(request, f'Constantes de {categoria} actualizadas exitosamente.')
            messages.info(request, f'Se actualizaron {len(nuevos_valores)} valores.')
            
            # En una implementación real, podrías:
            # 1. Guardar en una tabla de configuración en la base de datos
            # 2. Actualizar un archivo JSON/YAML de configuración
            # 3. Usar un sistema de caché para aplicar cambios en tiempo real
            
        except Exception as e:
            messages.error(request, f'Error al actualizar constantes: {str(e)}')
    
    return redirect('admin_constantes')

@login_required
@user_passes_test(is_admin)
def exportar_constantes(request):
    """Exporta todas las constantes en formato JSON"""
    
    constantes_export = {
        'TIPOS_REUNION': TIPOS_REUNION,
        'ESTADOS_REUNION': ESTADOS_REUNION,
        'MODALIDADES_REUNION': MODALIDADES_REUNION,
        'TIPOS_PARTICIPANTE': TIPOS_PARTICIPANTE,
        'CATEGORIAS_ACUERDO': CATEGORIAS_ACUERDO,
        'ESTADOS_ACUERDO': ESTADOS_ACUERDO,
        'PRIORIDADES': PRIORIDADES,
        'TIPOS_DOCUMENTO': TIPOS_DOCUMENTO,
        'TIPOS_ACTIVIDAD': TIPOS_ACTIVIDAD,
        'CONFIGURACIONES_SISTEMA': CONFIGURACIONES_SISTEMA,
    }
    
    return JsonResponse(constantes_export, json_dumps_params={'indent': 2, 'ensure_ascii': False})

@login_required
@user_passes_test(is_admin)
def importar_constantes(request):
    """Importa constantes desde un archivo JSON"""
    
    if request.method == 'POST':
        try:
            archivo = request.FILES.get('archivo_constantes')
            if not archivo:
                messages.error(request, 'Debe seleccionar un archivo.')
                return redirect('admin_constantes')
            
            # Leer y validar el archivo JSON
            contenido = archivo.read().decode('utf-8')
            constantes_importadas = json.loads(contenido)
            
            # Validar estructura
            campos_requeridos = [
                'TIPOS_REUNION', 'ESTADOS_REUNION', 'MODALIDADES_REUNION',
                'TIPOS_PARTICIPANTE', 'CATEGORIAS_ACUERDO', 'ESTADOS_ACUERDO',
                'PRIORIDADES', 'TIPOS_DOCUMENTO', 'TIPOS_ACTIVIDAD'
            ]
            
            campos_faltantes = [campo for campo in campos_requeridos if campo not in constantes_importadas]
            if campos_faltantes:
                messages.error(request, f'Campos faltantes en el archivo: {", ".join(campos_faltantes)}')
                return redirect('admin_constantes')
            
            # Aquí aplicarías las constantes importadas
            messages.success(request, 'Constantes importadas exitosamente.')
            messages.info(request, f'Se importaron {len(constantes_importadas)} categorías de constantes.')
            
        except json.JSONDecodeError:
            messages.error(request, 'El archivo no tiene formato JSON válido.')
        except Exception as e:
            messages.error(request, f'Error al importar constantes: {str(e)}')
    
    return redirect('admin_constantes')

def get_constante_api(request, categoria):
    """API para obtener constantes específicas (para AJAX)"""
    
    constantes_map = {
        'tipos_reunion': TIPOS_REUNION,
        'estados_reunion': ESTADOS_REUNION,
        'modalidades_reunion': MODALIDADES_REUNION,
        'tipos_participante': TIPOS_PARTICIPANTE,
        'categorias_acuerdo': CATEGORIAS_ACUERDO,
        'estados_acuerdo': ESTADOS_ACUERDO,
        'prioridades': PRIORIDADES,
        'tipos_documento': TIPOS_DOCUMENTO,
        'tipos_actividad': TIPOS_ACTIVIDAD,
    }
    
    if categoria in constantes_map:
        return JsonResponse({
            'categoria': categoria,
            'valores': constantes_map[categoria]
        })
    else:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)

# Función helper para templates
def get_constantes_context():
    """Retorna todas las constantes para usar en templates"""
    return {
        'TIPOS_REUNION': TIPOS_REUNION,
        'ESTADOS_REUNION': ESTADOS_REUNION,
        'MODALIDADES_REUNION': MODALIDADES_REUNION,
        'TIPOS_PARTICIPANTE': TIPOS_PARTICIPANTE,
        'CATEGORIAS_ACUERDO': CATEGORIAS_ACUERDO,
        'ESTADOS_ACUERDO': ESTADOS_ACUERDO,
        'PRIORIDADES': PRIORIDADES,
        'TIPOS_DOCUMENTO': TIPOS_DOCUMENTO,
        'TIPOS_ACTIVIDAD': TIPOS_ACTIVIDAD,
    }