from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from bson import ObjectId
from .models import ReunionNacional, Acuerdo, Participante, Documento
from .models import ParticipanteEmbebido, DocumentoEmbebido, SeguimientoEmbebido
from .constants import (
    TIPOS_REUNION, ESTADOS_REUNION, MODALIDADES_REUNION,
    TIPOS_PARTICIPANTE, CATEGORIAS_ACUERDO, ESTADOS_ACUERDO, 
    PRIORIDADES, TIPOS_DOCUMENTO, CATEGORIAS_FORMATIVAS, CURSOS_ESPECIFICOS,
    PLANTELES_TECNM, AREAS_DEPARTAMENTO, SEXOS
)
from .validators import (
    validar_fechas_reunion, validar_email_formato, validar_telefono,
    validar_url, validar_tamaño_archivo, validar_presupuesto,
    validar_participantes_esperados, validar_duplicado_email_participante,
    limpiar_y_validar_texto
)
from .validators import (
    validar_fechas_reunion, validar_email_formato, validar_telefono, 
    validar_url, validar_tamaño_archivo, validar_presupuesto, 
    validar_participantes_esperados, limpiar_y_validar_texto,
    validar_duplicado_email_participante
)

def index(request):
    """Dashboard principal del sistema de reuniones nacionales"""
    
    # Estadísticas generales
    total_reuniones = ReunionNacional.objects.count()
    reuniones_planificadas = ReunionNacional.objects.filter(estado='PLANIFICADA').count()
    reuniones_en_curso = ReunionNacional.objects.filter(estado='EN_CURSO').count()
    reuniones_finalizadas = ReunionNacional.objects.filter(estado='FINALIZADA').count()
    
    total_acuerdos = Acuerdo.objects.count()
    acuerdos_pendientes = Acuerdo.objects.filter(estado='PENDIENTE').count()
    acuerdos_en_proceso = Acuerdo.objects.filter(estado='EN_PROCESO').count()
    acuerdos_completados = Acuerdo.objects.filter(estado='COMPLETADO').count()
    
    total_participantes = Participante.objects.count()
    participantes_confirmados = Participante.objects.filter(confirmado=True).count()
    
    total_documentos = Documento.objects.count()
    
    # Reuniones próximas - las 10 más cercanas a la fecha actual (pasadas o futuras)
    from datetime import datetime
    from django.db.models import F
    from django.db.models.functions import Abs
    
    fecha_actual = datetime.now()
    
    # Obtener todas las reuniones y ordenarlas por cercanía a la fecha actual
    reuniones_proximas = sorted(
        ReunionNacional.objects.all(),
        key=lambda r: abs((r.fecha_inicio - fecha_actual).total_seconds()) if r.fecha_inicio else float('inf')
    )[:10]
    
    # Acuerdos recientes
    acuerdos_recientes = Acuerdo.objects.order_by('-fecha_creacion')[:5]
    
    # Acuerdos por categoría
    acuerdos_por_categoria = {}
    for categoria in Acuerdo.CATEGORIAS:
        acuerdos_por_categoria[categoria[1]] = Acuerdo.objects.filter(categoria=categoria[0]).count()
    
    context = {
        'total_reuniones': total_reuniones,
        'reuniones_planificadas': reuniones_planificadas,
        'reuniones_en_curso': reuniones_en_curso,
        'reuniones_finalizadas': reuniones_finalizadas,
        'total_acuerdos': total_acuerdos,
        'acuerdos_pendientes': acuerdos_pendientes,
        'acuerdos_en_proceso': acuerdos_en_proceso,
        'acuerdos_completados': acuerdos_completados,
        'total_participantes': total_participantes,
        'participantes_confirmados': participantes_confirmados,
        'total_documentos': total_documentos,
        'reuniones_proximas': reuniones_proximas,
        'acuerdos_recientes': acuerdos_recientes,
        'acuerdos_por_categoria': acuerdos_por_categoria,
    }
    
    return render(request, 'mi_aplication/index_reuniones.html', context)

def lista_reuniones(request):
    """Lista todas las reuniones nacionales"""
    
    reuniones = ReunionNacional.objects.all()
    
    # Filtros
    tipo = request.GET.get('tipo')
    estado = request.GET.get('estado')
    sede = request.GET.get('sede')
    
    if tipo:
        reuniones = reuniones.filter(tipo=tipo)
    if estado:
        reuniones = reuniones.filter(estado=estado)
    if sede:
        reuniones = reuniones.filter(sede__icontains=sede)
    
    # Convertir a lista para paginación
    reuniones_list = list(reuniones)
    
    # Paginación manual
    paginator = Paginator(reuniones_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipos_reunion': ReunionNacional.TIPOS_REUNION,
        'estados': ReunionNacional.ESTADOS,
    }
    
    return render(request, 'mi_aplication/lista_reuniones.html', context)

def detalle_reunion(request, reunion_id):
    """Muestra el detalle completo de una reunión"""
    try:
        from bson import ObjectId
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    # Obtener acuerdos relacionados
    acuerdos = Acuerdo.objects.filter(reunion=reunion)
    
    # Estadísticas de la reunión
    participantes_confirmados = reunion.participantes_confirmados_count()
    acuerdos_completados = acuerdos.filter(estado='COMPLETADO').count()
    
    context = {
        'reunion': reunion,
        'acuerdos': acuerdos,
        'participantes_confirmados': participantes_confirmados,
        'acuerdos_completados': acuerdos_completados,
    }
    
    return render(request, 'mi_aplication/detalle_reunion.html', context)

def crear_reunion(request):
    """Crea una nueva reunión nacional"""
    if request.method == 'POST':
        errores_validacion = []
        
        try:
            # Obtener y limpiar datos del formulario
            titulo, errores_titulo = limpiar_y_validar_texto(
                request.POST.get('titulo'), 'título', max_length=200, required=True
            )
            errores_validacion.extend(errores_titulo)
            
            tipo = request.POST.get('tipo')
            estado = request.POST.get('estado')
            
            # Validar fechas
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_fin_str = request.POST.get('fecha_fin')
            
            if not fecha_inicio_str or not fecha_fin_str:
                errores_validacion.append("Las fechas de inicio y fin son obligatorias.")
                if errores_validacion:
                    for error in errores_validacion:
                        messages.error(request, error)
                    context = {
                        'tipos_reunion': ReunionNacional.TIPOS_REUNION,
                        'estados': ReunionNacional.ESTADOS,
                        'modalidades': ReunionNacional.MODALIDADES,
                    }
                    return render(request, 'mi_aplication/crear_reunion.html', context)
            
            # Parsear fechas y asegurar que tengan timezone
            fecha_inicio_naive = datetime.fromisoformat(fecha_inicio_str.replace('T', ' '))
            fecha_fin_naive = datetime.fromisoformat(fecha_fin_str.replace('T', ' '))
            
            # Convertir a fechas con timezone
            fecha_inicio = timezone.make_aware(fecha_inicio_naive) if timezone.is_naive(fecha_inicio_naive) else fecha_inicio_naive
            fecha_fin = timezone.make_aware(fecha_fin_naive) if timezone.is_naive(fecha_fin_naive) else fecha_fin_naive
            
            # Validar fechas
            errores_fechas = validar_fechas_reunion(fecha_inicio, fecha_fin)
            errores_validacion.extend(errores_fechas)
            
            sede, errores_sede = limpiar_y_validar_texto(
                request.POST.get('sede'), 'sede', max_length=200, required=True
            )
            errores_validacion.extend(errores_sede)
            
            descripcion, errores_desc = limpiar_y_validar_texto(
                request.POST.get('descripcion'), 'descripción', max_length=1000, required=False
            )
            errores_validacion.extend(errores_desc)
            
            objetivos, errores_obj = limpiar_y_validar_texto(
                request.POST.get('objetivos'), 'objetivos', max_length=1000, required=False
            )
            errores_validacion.extend(errores_obj)
            
            organizador_principal, errores_org = limpiar_y_validar_texto(
                request.POST.get('organizador_principal'), 'organizador principal', max_length=200, required=False
            )
            errores_validacion.extend(errores_org)
            organizador_principal = organizador_principal or None
            
            # Validar participantes esperados
            participantes_esperados_str = request.POST.get('participantes_esperados', '0')
            error_participantes = validar_participantes_esperados(participantes_esperados_str)
            if error_participantes:
                errores_validacion.append(error_participantes)
                participantes_esperados = 0
            else:
                participantes_esperados = int(participantes_esperados_str) if participantes_esperados_str else 0
            
            # Validar presupuesto
            presupuesto_str = request.POST.get('presupuesto_asignado')
            error_presupuesto = validar_presupuesto(presupuesto_str)
            if error_presupuesto:
                errores_validacion.append(error_presupuesto)
                presupuesto_asignado = None
            else:
                presupuesto_asignado = float(presupuesto_str) if presupuesto_str else None
            
            modalidad = request.POST.get('modalidad', 'PRESENCIAL')
            
            # Validar URL de videollamada si es necesario
            enlace_videollamada = request.POST.get('enlace_videollamada')
            if enlace_videollamada:
                error_url = validar_url(enlace_videollamada)
                if error_url:
                    errores_validacion.append(f"Enlace de videollamada: {error_url}")
                    enlace_videollamada = None
            else:
                enlace_videollamada = None
            
            direccion_fisica, errores_dir = limpiar_y_validar_texto(
                request.POST.get('direccion_fisica'), 'dirección física', max_length=500, required=False
            )
            errores_validacion.extend(errores_dir)
            direccion_fisica = direccion_fisica or None
            
            # Si hay errores de validación, mostrarlos y no crear la reunión
            if errores_validacion:
                for error in errores_validacion:
                    messages.error(request, error)
                context = {
                    'tipos_reunion': TIPOS_REUNION,
                    'estados': ESTADOS_REUNION,
                    'modalidades': MODALIDADES_REUNION,
                }
                return render(request, 'mi_aplication/crear_reunion.html', context)
            
            # Crear la reunión
            reunion = ReunionNacional(
                titulo=titulo,
                tipo=tipo,
                estado=estado,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                sede=sede,
                modalidad=modalidad,
                enlace_videollamada=enlace_videollamada,
                direccion_fisica=direccion_fisica,
                descripcion=descripcion,
                objetivos=objetivos,
                organizador_principal=organizador_principal,
                participantes_esperados=participantes_esperados,
                presupuesto_asignado=presupuesto_asignado,
                participantes=[],
                agenda=[],
                documentos=[]
            )
            reunion.save()
            
            messages.success(request, f'Reunión "{titulo}" creada exitosamente.')
            return redirect('detalle_reunion', reunion_id=reunion.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear la reunión: {str(e)}')
    
    context = {
        'tipos_reunion': TIPOS_REUNION,
        'estados': ESTADOS_REUNION,
        'modalidades': MODALIDADES_REUNION,
    }
    
    return render(request, 'mi_aplication/crear_reunion.html', context)

def editar_reunion(request, reunion_id):
    """Edita una reunión existente"""
    try:
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            
            # Actualizar datos del formulario
            reunion.titulo = request.POST.get('titulo')
            reunion.tipo = request.POST.get('tipo')
            reunion.estado = request.POST.get('estado')
            reunion.fecha_inicio = datetime.fromisoformat(request.POST.get('fecha_inicio').replace('T', ' '))
            reunion.fecha_fin = datetime.fromisoformat(request.POST.get('fecha_fin').replace('T', ' '))
            reunion.sede = request.POST.get('sede')
            reunion.descripcion = request.POST.get('descripcion')
            reunion.objetivos = request.POST.get('objetivos')
            reunion.organizador_principal = request.POST.get('organizador_principal') or None
            reunion.participantes_esperados = int(request.POST.get('participantes_esperados', 0))
            reunion.presupuesto_asignado = float(request.POST.get('presupuesto_asignado', 0)) if request.POST.get('presupuesto_asignado') else None
            reunion.modalidad = request.POST.get('modalidad', 'PRESENCIAL')
            reunion.enlace_videollamada = request.POST.get('enlace_videollamada') or None
            reunion.direccion_fisica = request.POST.get('direccion_fisica') or None
            reunion.fecha_actualizacion = timezone.now()
            
            reunion.save()
            
            messages.success(request, f'Reunión "{reunion.titulo}" actualizada exitosamente.')
            return redirect('detalle_reunion', reunion_id=reunion.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la reunión: {str(e)}')
    
    context = {
        'reunion': reunion,
        'tipos_reunion': ReunionNacional.TIPOS_REUNION,
        'estados': ReunionNacional.ESTADOS,
        'modalidades': ReunionNacional.MODALIDADES,
    }
    
    return render(request, 'mi_aplication/editar_reunion.html', context)

def subir_documento_reunion(request, reunion_id):
    """Sube un documento a una reunión"""
    try:
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            # Crear documento embebido
            tamaño_str = request.POST.get('tamaño', '0')
            tamaño = int(tamaño_str) if tamaño_str and tamaño_str.strip() else 0
            
            documento = DocumentoEmbebido(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                tipo=request.POST.get('tipo'),
                url=request.POST.get('url', ''),
                formato=request.POST.get('formato', ''),
                tamaño=tamaño,
                version=request.POST.get('version', '1.0'),
                subido_por=request.POST.get('subido_por', 'Sistema'),
                observaciones=request.POST.get('observaciones', '')
            )
            
            # Agregar a la lista de documentos de la reunión
            reunion.documentos.append(documento)
            reunion.save()
            
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('detalle_reunion', reunion_id=reunion.id)
            
        except Exception as e:
            messages.error(request, f'Error al subir el documento: {str(e)}')
    
    context = {
        'reunion': reunion,
        'tipos_documento': TIPOS_DOCUMENTO
    }
    
    return render(request, 'mi_aplication/subir_documento_reunion.html', context)

def agregar_participante_reunion(request, reunion_id):
    """Agrega un participante a una reunión"""
    try:
        from bson import ObjectId
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            # Crear participante embebido
            participante = ParticipanteEmbebido(
                nombre=request.POST.get('nombre'),
                apellido_paterno=request.POST.get('apellido_paterno'),
                apellido_materno=request.POST.get('apellido_materno', ''),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono', ''),
                instituto=request.POST.get('instituto'),
                departamento=request.POST.get('departamento', ''),
                tipo_participante=request.POST.get('tipo_participante'),
                confirmado=request.POST.get('confirmado') == 'on',
                observaciones=request.POST.get('observaciones', '')
            )
            
            # Agregar a la lista de participantes de la reunión
            reunion.participantes.append(participante)
            reunion.save()
            
            messages.success(request, 'Participante agregado exitosamente.')
            return redirect('detalle_reunion', reunion_id=reunion.id)
            
        except Exception as e:
            messages.error(request, f'Error al agregar el participante: {str(e)}')
    
    context = {
        'reunion': reunion,
        'tipos_participante': TIPOS_PARTICIPANTE,
    }
    
    return render(request, 'mi_aplication/agregar_participante_reunion.html', context)

def agregar_participante_existente_reunion(request, reunion_id):
    """Agrega un participante existente a una reunión"""
    try:
        from bson import ObjectId
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            participante_id = request.POST.get('participante_id')
            if participante_id:
                # Obtener el participante existente
                participante = Participante.objects.get(id=ObjectId(participante_id))
                
                # Crear participante embebido basado en el existente
                participante_embebido = ParticipanteEmbebido(
                    nombre=participante.nombre,
                    apellido_paterno=participante.apellido_paterno,
                    apellido_materno=participante.apellido_materno,
                    email=participante.email,
                    telefono=participante.telefono,
                    plantel_tecnm=participante.plantel_tecnm if hasattr(participante, 'plantel_tecnm') and participante.plantel_tecnm else 'OTRO_PLANTEL',
                    area_departamento=participante.area_departamento if hasattr(participante, 'area_departamento') else None,
                    tipo_participante=participante.tipo_participante,
                    confirmado=participante.confirmado,
                    observaciones=participante.observaciones
                )
                
                # Agregar a la lista de participantes de la reunión
                reunion.participantes.append(participante_embebido)
                reunion.save()
                
                messages.success(request, f'Participante "{participante.nombre} {participante.apellido_paterno}" agregado exitosamente a la reunión.')
                return redirect('detalle_reunion', reunion_id=reunion.id)
            else:
                messages.error(request, 'Debes seleccionar un participante.')
                
        except Exception as e:
            messages.error(request, f'Error al agregar el participante: {str(e)}')
    
    # Obtener todos los participantes disponibles
    participantes_disponibles = Participante.objects.all().order_by('apellido_paterno', 'nombre')
    
    # Filtrar participantes que ya están en la reunión
    participantes_en_reunion = [p.email for p in reunion.participantes]
    participantes_disponibles = [p for p in participantes_disponibles if p.email not in participantes_en_reunion]
    
    context = {
        'reunion': reunion,
        'participantes_disponibles': participantes_disponibles,
        'tipos_participante': [
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('Docente TecNM', 'Docente TecNM'),
            ('Matemáticas y Ciencias Básicas', 'Matemáticas y Ciencias Básicas'),
            ('INVITADO', 'Invitado'),
        ]
    }
    
    return render(request, 'mi_aplication/agregar_participante_existente_reunion.html', context)

def lista_acuerdos(request):
    """Lista todos los acuerdos"""
    acuerdos = Acuerdo.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    categoria = request.GET.get('categoria')
    estado = request.GET.get('estado')
    reunion = request.GET.get('reunion')
    
    if categoria:
        acuerdos = acuerdos.filter(categoria=categoria)
    if estado:
        acuerdos = acuerdos.filter(estado=estado)
    if reunion:
        acuerdos = acuerdos.filter(reunion__titulo__icontains=reunion)
    
    # Convertir a lista para paginación
    acuerdos_list = list(acuerdos)
    
    # Paginación manual
    paginator = Paginator(acuerdos_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categorias': Acuerdo.CATEGORIAS,
        'estados_acuerdo': Acuerdo.ESTADOS_ACUERDO,
    }
    
    return render(request, 'mi_aplication/lista_acuerdos.html', context)

def detalle_acuerdo(request, acuerdo_id):
    """Muestra el detalle de un acuerdo"""
    try:
        from bson import ObjectId
        acuerdo = Acuerdo.objects.get(id=ObjectId(acuerdo_id))
    except (Acuerdo.DoesNotExist, ValueError):
        messages.error(request, 'Acuerdo no encontrado.')
        return redirect('lista_acuerdos')
    
    context = {
        'acuerdo': acuerdo,
    }
    
    return render(request, 'mi_aplication/detalle_acuerdo.html', context)

def subir_documento_acuerdo(request, acuerdo_id):
    """Sube un documento a un acuerdo"""
    try:
        from bson import ObjectId
        acuerdo = Acuerdo.objects.get(id=ObjectId(acuerdo_id))
    except (Acuerdo.DoesNotExist, ValueError):
        messages.error(request, 'Acuerdo no encontrado.')
        return redirect('lista_acuerdos')
    
    if request.method == 'POST':
        try:
            # Crear documento embebido
            tamaño_str = request.POST.get('tamaño', '0')
            tamaño = int(tamaño_str) if tamaño_str and tamaño_str.strip() else 0
            
            documento = DocumentoEmbebido(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                tipo=request.POST.get('tipo'),
                url=request.POST.get('url', ''),
                formato=request.POST.get('formato', ''),
                tamaño=tamaño,
                version=request.POST.get('version', '1.0'),
                subido_por=request.POST.get('subido_por', 'Sistema'),
                observaciones=request.POST.get('observaciones', '')
            )
            
            # Agregar a la lista de documentos del acuerdo
            acuerdo.documentos.append(documento)
            acuerdo.save()
            
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('detalle_acuerdo', acuerdo_id=acuerdo.id)
            
        except Exception as e:
            messages.error(request, f'Error al subir el documento: {str(e)}')
    
    context = {
        'acuerdo': acuerdo,
        'tipos_documento': TIPOS_DOCUMENTO
    }
    
    return render(request, 'mi_aplication/subir_documento_acuerdo.html', context)

def lista_participantes(request):
    """Lista todos los participantes"""
    participantes = Participante.objects.all().order_by('apellido_paterno', 'nombre')
    
    # Filtros
    tipo = request.GET.get('tipo')
    confirmado = request.GET.get('confirmado')
    plantel = request.GET.get('plantel')
    
    if tipo:
        participantes = participantes.filter(tipo_participante=tipo)
    if confirmado:
        participantes = participantes.filter(confirmado=confirmado == 'true')
    if plantel:
        participantes = participantes.filter(plantel_tecnm=plantel)
    
    # Convertir a lista para paginación
    participantes_list = list(participantes)
    
    # Paginación manual
    paginator = Paginator(participantes_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipos_participante': TIPOS_PARTICIPANTE,
    }
    
    return render(request, 'mi_aplication/lista_participantes.html', context)

def crear_participante(request):
    """Crea un nuevo participante"""
    if request.method == 'POST':
        errores_validacion = []
        
        try:
            # Validar y limpiar datos
            nombre, errores_nombre = limpiar_y_validar_texto(
                request.POST.get('nombre'), 'nombre', max_length=100, required=True
            )
            errores_validacion.extend(errores_nombre)
            
            apellido_paterno, errores_ap = limpiar_y_validar_texto(
                request.POST.get('apellido_paterno'), 'apellido paterno', max_length=100, required=True
            )
            errores_validacion.extend(errores_ap)
            
            apellido_materno, errores_am = limpiar_y_validar_texto(
                request.POST.get('apellido_materno'), 'apellido materno', max_length=100, required=False
            )
            errores_validacion.extend(errores_am)
            
            # Validar email
            email = request.POST.get('email', '').strip()
            if not email:
                errores_validacion.append("El email es obligatorio.")
            else:
                error_email_formato = validar_email_formato(email)
                if error_email_formato:
                    errores_validacion.append(error_email_formato)
                else:
                    # Validar email duplicado
                    error_email_duplicado = validar_duplicado_email_participante(email)
                    if error_email_duplicado:
                        errores_validacion.append(error_email_duplicado)
            
            # Validar teléfono
            telefono = request.POST.get('telefono', '').strip()
            error_telefono = validar_telefono(telefono)
            if error_telefono:
                errores_validacion.append(error_telefono)
            
            instituto, errores_inst = limpiar_y_validar_texto(
                request.POST.get('instituto'), 'instituto', max_length=200, required=True
            )
            errores_validacion.extend(errores_inst)
            
            departamento, errores_dept = limpiar_y_validar_texto(
                request.POST.get('departamento'), 'departamento', max_length=100, required=False
            )
            errores_validacion.extend(errores_dept)
            
            tipo_participante = request.POST.get('tipo_participante')
            if not tipo_participante:
                errores_validacion.append("El tipo de participante es obligatorio.")
            
            observaciones, errores_obs = limpiar_y_validar_texto(
                request.POST.get('observaciones'), 'observaciones', max_length=500, required=False
            )
            errores_validacion.extend(errores_obs)
            
            # Si hay errores de validación, mostrarlos y no crear el participante
            if errores_validacion:
                for error in errores_validacion:
                    messages.error(request, error)
                context = {
                    'tipos_participante': [
                        ('DIRECTOR', 'Director'),
                        ('SUBDIRECTOR', 'Subdirector'),
                        ('COORDINADOR', 'Coordinador'),
                        ('DOCENTE', 'Docente'),
                        ('ADMINISTRATIVO', 'Administrativo'),
                        ('Docente TecNM', 'Docente TecNM'),
                        ('Matemáticas y Ciencias Básicas', 'Matemáticas y Ciencias Básicas'),
                        ('INVITADO', 'Invitado'),
                    ]
                }
                return render(request, 'mi_aplication/crear_participante.html', context)
            
            # Crear participante si no hay errores
            participante = Participante(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno or '',
                email=email,
                telefono=telefono or '',
                instituto=instituto,
                departamento=departamento or '',
                tipo_participante=tipo_participante,
                confirmado=request.POST.get('confirmado') == 'on',
                observaciones=observaciones or ''
            )
            participante.save()
            
            messages.success(request, f'Participante "{participante.nombre} {participante.apellido_paterno}" creado exitosamente.')
            return redirect('lista_participantes')
            
        except Exception as e:
            messages.error(request, f'Error al crear el participante: {str(e)}')
    
    context = {
        'tipos_participante': TIPOS_PARTICIPANTE,
    }
    
    return render(request, 'mi_aplication/crear_participante.html', context)

def editar_participante(request, participante_id):
    """Edita un participante existente"""
    try:
        from bson import ObjectId
        participante = Participante.objects.get(id=ObjectId(participante_id))
    except (Participante.DoesNotExist, ValueError):
        messages.error(request, 'Participante no encontrado.')
        return redirect('lista_participantes')
    
    if request.method == 'POST':
        try:
            # Actualizar datos básicos del participante
            participante.nombre = request.POST.get('nombre')
            participante.apellido_paterno = request.POST.get('apellido_paterno')
            participante.apellido_materno = request.POST.get('apellido_materno', '')
            participante.email = request.POST.get('email')
            participante.telefono = request.POST.get('telefono', '')
            participante.tipo_participante = request.POST.get('tipo_participante')
            participante.confirmado = request.POST.get('confirmado') == 'on'
            participante.observaciones = request.POST.get('observaciones', '')
            
            # Datos de identificación
            rfc = request.POST.get('rfc', '').strip()
            participante.rfc = rfc if rfc else None
            
            curp = request.POST.get('curp', '').strip()
            participante.curp = curp if curp else None
            
            sexo = request.POST.get('sexo', '')
            participante.sexo = sexo if sexo else None
            
            edad = request.POST.get('edad', '')
            participante.edad = int(edad) if edad else None
            
            # Datos institucionales
            plantel_tecnm = request.POST.get('plantel_tecnm', '')
            participante.plantel_tecnm = plantel_tecnm if plantel_tecnm else None
            
            area_departamento = request.POST.get('area_departamento', '')
            participante.area_departamento = area_departamento if area_departamento else None
            
            participante.puesto = request.POST.get('puesto', '')
            participante.director = request.POST.get('director', '')
            participante.correo_direccion = request.POST.get('correo_direccion', '')
            participante.jefe_inmediato = request.POST.get('jefe_inmediato', '')
            participante.correo_jefe_inmediato = request.POST.get('correo_jefe_inmediato', '')
            
            # Actualizar campos de capacitación
            categoria_formativa = request.POST.get('categoria_formativa', '')
            if categoria_formativa:
                participante.categoria_formativa = categoria_formativa
            else:
                participante.categoria_formativa = None
            
            # Cursos específicos (múltiples selecciones)
            cursos_especificos = request.POST.getlist('cursos_especificos')
            participante.cursos_especificos = cursos_especificos if cursos_especificos else []
            
            participante.save()
            
            messages.success(request, f'Participante "{participante.nombre} {participante.apellido_paterno}" actualizado exitosamente.')
            return redirect('lista_participantes')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el participante: {str(e)}')
    
    context = {
        'participante': participante,
        'tipos_participante': TIPOS_PARTICIPANTE,
        'categorias_formativas': CATEGORIAS_FORMATIVAS,
        'cursos_especificos': CURSOS_ESPECIFICOS,
        'planteles_tecnm': PLANTELES_TECNM,
        'areas_departamento': AREAS_DEPARTAMENTO,
        'sexos': SEXOS,
    }
    
    return render(request, 'mi_aplication/editar_participante.html', context)

def eliminar_participante(request, participante_id):
    """Elimina un participante"""
    try:
        from bson import ObjectId
        participante = Participante.objects.get(id=ObjectId(participante_id))
    except (Participante.DoesNotExist, ValueError):
        messages.error(request, 'Participante no encontrado.')
        return redirect('lista_participantes')
    
    if request.method == 'POST':
        try:
            nombre_completo = f"{participante.nombre} {participante.apellido_paterno}"
            participante.delete()
            messages.success(request, f'Participante "{nombre_completo}" eliminado exitosamente.')
            return redirect('lista_participantes')
        except Exception as e:
            messages.error(request, f'Error al eliminar el participante: {str(e)}')
    
    context = {
        'participante': participante
    }
    
    return render(request, 'mi_aplication/eliminar_participante.html', context)

def detalle_participante(request, participante_id):
    """Muestra el detalle de un participante"""
    try:
        from bson import ObjectId
        participante = Participante.objects.get(id=ObjectId(participante_id))
    except (Participante.DoesNotExist, ValueError):
        messages.error(request, 'Participante no encontrado.')
        return redirect('lista_participantes')
    
    # Obtener reuniones donde participa
    reuniones = ReunionNacional.objects.filter(participantes__email=participante.email)
    
    context = {
        'participante': participante,
        'reuniones': reuniones
    }
    
    return render(request, 'mi_aplication/detalle_participante.html', context)

def lista_documentos(request):
    """Lista todos los documentos"""
    documentos = Documento.objects.all().order_by('-fecha_subida')
    
    # Filtros
    tipo = request.GET.get('tipo')
    reunion = request.GET.get('reunion')
    fecha = request.GET.get('fecha')
    
    if tipo:
        documentos = documentos.filter(tipo=tipo)
    if reunion:
        documentos = documentos.filter(reunion__titulo__icontains=reunion)
    if fecha:
        documentos = documentos.filter(fecha_subida__date=fecha)
    
    # Convertir a lista para paginación
    documentos_list = list(documentos)
    
    # Paginación manual
    paginator = Paginator(documentos_list, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipos_documento': TIPOS_DOCUMENTO
    }
    
    return render(request, 'mi_aplication/lista_documentos.html', context)

def estadisticas(request):
    """Página de estadísticas del sistema"""
    
    # Totales
    total_reuniones = ReunionNacional.objects.count()
    total_acuerdos = Acuerdo.objects.count()
    total_participantes = Participante.objects.count()
    total_documentos = Documento.objects.count()
    
    # Estadísticas de reuniones
    reuniones_por_tipo = {}
    for tipo in ReunionNacional.TIPOS_REUNION:
        count = ReunionNacional.objects.filter(tipo=tipo[0]).count()
        if count > 0:  # Solo mostrar tipos con datos
            reuniones_por_tipo[tipo[1]] = count
    
    reuniones_por_estado = {}
    for estado in ReunionNacional.ESTADOS:
        count = ReunionNacional.objects.filter(estado=estado[0]).count()
        if count > 0:  # Solo mostrar estados con datos
            reuniones_por_estado[estado[1]] = count
    
    # Estadísticas de acuerdos
    acuerdos_por_categoria = {}
    for categoria in Acuerdo.CATEGORIAS:
        count = Acuerdo.objects.filter(categoria=categoria[0]).count()
        if count > 0:  # Solo mostrar categorías con datos
            acuerdos_por_categoria[categoria[1]] = count
    
    acuerdos_por_estado = {}
    for estado in Acuerdo.ESTADOS_ACUERDO:
        count = Acuerdo.objects.filter(estado=estado[0]).count()
        if count > 0:  # Solo mostrar estados con datos
            acuerdos_por_estado[estado[1]] = count
    
    # Estadísticas de participantes
    participantes_por_tipo = {}
    for tipo in TIPOS_PARTICIPANTE:
        count = Participante.objects.filter(tipo_participante=tipo[0]).count()
        if count > 0:  # Solo mostrar tipos con datos
            participantes_por_tipo[tipo[1]] = count
    
    # Estadísticas adicionales
    participantes_confirmados = Participante.objects.filter(confirmado=True).count()
    participantes_pendientes = total_participantes - participantes_confirmados
    
    # Reuniones por modalidad
    reuniones_por_modalidad = {}
    for modalidad in ReunionNacional.MODALIDADES:
        count = ReunionNacional.objects.filter(modalidad=modalidad[0]).count()
        if count > 0:
            reuniones_por_modalidad[modalidad[1]] = count
    
    # Acuerdos por prioridad
    acuerdos_por_prioridad = {}
    prioridades = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    for prioridad in prioridades:
        count = Acuerdo.objects.filter(prioridad=prioridad[0]).count()
        if count > 0:
            acuerdos_por_prioridad[prioridad[1]] = count
    
    # Documentos por tipo
    documentos_por_tipo = {}
    for tipo in TIPOS_DOCUMENTO:
        count = Documento.objects.filter(tipo=tipo[0]).count()
        if count > 0:
            documentos_por_tipo[tipo[1]] = count
    
    # Reuniones recientes (últimos 30 días)
    from datetime import datetime, timedelta
    fecha_limite = datetime.now() - timedelta(days=30)
    reuniones_recientes = ReunionNacional.objects.filter(fecha_inicio__gte=fecha_limite).count()
    
    # Acuerdos vencidos
    acuerdos_vencidos = Acuerdo.objects.filter(fecha_limite__lt=datetime.now(), estado__in=['PENDIENTE', 'EN_PROCESO']).count()
    
    context = {
        'total_reuniones': total_reuniones,
        'total_acuerdos': total_acuerdos,
        'total_participantes': total_participantes,
        'total_documentos': total_documentos,
        'reuniones_por_tipo': reuniones_por_tipo,
        'reuniones_por_estado': reuniones_por_estado,
        'reuniones_por_modalidad': reuniones_por_modalidad,
        'acuerdos_por_categoria': acuerdos_por_categoria,
        'acuerdos_por_estado': acuerdos_por_estado,
        'acuerdos_por_prioridad': acuerdos_por_prioridad,
        'participantes_por_tipo': participantes_por_tipo,
        'documentos_por_tipo': documentos_por_tipo,
        'participantes_confirmados': participantes_confirmados,
        'participantes_pendientes': participantes_pendientes,
        'reuniones_recientes': reuniones_recientes,
        'acuerdos_vencidos': acuerdos_vencidos,
    }
    
    return render(request, 'mi_aplication/estadisticas.html', context)

def buscar(request):
    """Búsqueda general en el sistema"""
    query = request.GET.get('q', '')
    resultados = {}
    
    if query:
        # Buscar en reuniones
        reuniones = ReunionNacional.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(sede__icontains=query)
        )[:10]
        resultados['reuniones'] = list(reuniones)
        
        # Buscar en acuerdos
        acuerdos = Acuerdo.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(responsable__icontains=query)
        )[:10]
        resultados['acuerdos'] = list(acuerdos)
        
        # Buscar en participantes
        participantes = Participante.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido_paterno__icontains=query) |
            Q(apellido_materno__icontains=query) |
            Q(email__icontains=query)
        )[:10]
        resultados['participantes'] = list(participantes)
        
        # Buscar en documentos
        documentos = Documento.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )[:10]
        resultados['documentos'] = list(documentos)
    
    context = {
        'query': query,
        'resultados': resultados,
    }
    
    return render(request, 'mi_aplication/buscar.html', context)

# ========== FUNCIONES CRUD FALTANTES ==========

def crear_acuerdo(request):
    """Crea un nuevo acuerdo"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion', '')
            categoria = request.POST.get('categoria')
            estado = request.POST.get('estado', 'PENDIENTE')
            prioridad = request.POST.get('prioridad', 'MEDIA')
            responsable = request.POST.get('responsable', '')
            fecha_limite_str = request.POST.get('fecha_limite')
            reunion_id = request.POST.get('reunion_id')
            
            # Convertir fecha_limite
            fecha_limite = None
            if fecha_limite_str:
                fecha_limite = datetime.fromisoformat(fecha_limite_str.replace('T', ' '))
            
            # Obtener reunión si se especifica
            reunion = None
            if reunion_id:
                try:
                    reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
                except ReunionNacional.DoesNotExist:
                    messages.error(request, 'Reunión no encontrada.')
                    return redirect('crear_acuerdo')
            
            # Crear el acuerdo
            acuerdo = Acuerdo(
                titulo=titulo,
                descripcion=descripcion,
                categoria=categoria,
                estado=estado,
                prioridad=prioridad,
                responsable=responsable,
                fecha_limite=fecha_limite,
                reunion=reunion,
                seguimientos=[],
                documentos=[]
            )
            acuerdo.save()
            
            messages.success(request, f'Acuerdo "{titulo}" creado exitosamente.')
            return redirect('detalle_acuerdo', acuerdo_id=acuerdo.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear el acuerdo: {str(e)}')
    
    # Obtener reuniones para el select
    reuniones = ReunionNacional.objects.all().order_by('-fecha_inicio')
    
    context = {
        'reuniones': reuniones,
        'categorias': Acuerdo.CATEGORIAS,
        'estados_acuerdo': Acuerdo.ESTADOS_ACUERDO,
        'prioridades': Acuerdo.PRIORIDADES,
    }
    
    return render(request, 'mi_aplication/crear_acuerdo.html', context)

def editar_acuerdo(request, acuerdo_id):
    """Edita un acuerdo existente"""
    try:
        acuerdo = Acuerdo.objects.get(id=ObjectId(acuerdo_id))
    except (Acuerdo.DoesNotExist, ValueError):
        messages.error(request, 'Acuerdo no encontrado.')
        return redirect('lista_acuerdos')
    
    if request.method == 'POST':
        try:
            # Actualizar datos del formulario
            acuerdo.titulo = request.POST.get('titulo')
            acuerdo.descripcion = request.POST.get('descripcion', '')
            acuerdo.categoria = request.POST.get('categoria')
            acuerdo.estado = request.POST.get('estado')
            acuerdo.prioridad = request.POST.get('prioridad')
            acuerdo.responsable = request.POST.get('responsable', '')
            
            fecha_limite_str = request.POST.get('fecha_limite')
            if fecha_limite_str:
                acuerdo.fecha_limite = datetime.fromisoformat(fecha_limite_str.replace('T', ' '))
            else:
                acuerdo.fecha_limite = None
            
            reunion_id = request.POST.get('reunion_id')
            if reunion_id:
                try:
                    acuerdo.reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
                except ReunionNacional.DoesNotExist:
                    acuerdo.reunion = None
            else:
                acuerdo.reunion = None
            
            acuerdo.fecha_actualizacion = timezone.now()
            acuerdo.save()
            
            messages.success(request, f'Acuerdo "{acuerdo.titulo}" actualizado exitosamente.')
            return redirect('detalle_acuerdo', acuerdo_id=acuerdo.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el acuerdo: {str(e)}')
    
    # Obtener reuniones para el select
    reuniones = ReunionNacional.objects.all().order_by('-fecha_inicio')
    
    context = {
        'acuerdo': acuerdo,
        'reuniones': reuniones,
        'categorias': Acuerdo.CATEGORIAS,
        'estados_acuerdo': Acuerdo.ESTADOS_ACUERDO,
        'prioridades': Acuerdo.PRIORIDADES,
    }
    
    return render(request, 'mi_aplication/editar_acuerdo.html', context)

def eliminar_reunion(request, reunion_id):
    """Elimina una reunión"""
    try:
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            # Verificar si hay acuerdos asociados
            acuerdos_asociados = Acuerdo.objects.filter(reunion=reunion).count()
            if acuerdos_asociados > 0:
                messages.warning(request, f'No se puede eliminar la reunión porque tiene {acuerdos_asociados} acuerdo(s) asociado(s). Elimina primero los acuerdos.')
                return redirect('detalle_reunion', reunion_id=reunion.id)
            
            titulo = reunion.titulo
            reunion.delete()
            
            messages.success(request, f'Reunión "{titulo}" eliminada exitosamente.')
            return redirect('lista_reuniones')
            
        except Exception as e:
            messages.error(request, f'Error al eliminar la reunión: {str(e)}')
    
    context = {
        'reunion': reunion,
    }
    
    return render(request, 'mi_aplication/eliminar_reunion.html', context)

def crear_documento(request):
    """Crea un nuevo documento independiente"""
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion', '')
            tipo = request.POST.get('tipo')
            url = request.POST.get('url', '')
            formato = request.POST.get('formato', '')
            tamaño_str = request.POST.get('tamaño', '0')
            tamaño = int(tamaño_str) if tamaño_str and tamaño_str.strip() else 0
            version = request.POST.get('version', '1.0')
            autor = request.POST.get('autor', '')
            palabras_clave = request.POST.get('palabras_clave', '')
            
            # Crear el documento
            documento = Documento(
                titulo=titulo,
                descripcion=descripcion,
                tipo=tipo,
                url=url,
                formato=formato,
                tamaño=tamaño,
                version=version,
                autor=autor,
                palabras_clave=palabras_clave
            )
            documento.save()
            
            messages.success(request, f'Documento "{titulo}" creado exitosamente.')
            return redirect('detalle_documento', documento_id=documento.id)
            
        except Exception as e:
            messages.error(request, f'Error al crear el documento: {str(e)}')
    
    context = {
        'tipos_documento': TIPOS_DOCUMENTO
    }
    
    return render(request, 'mi_aplication/crear_documento.html', context)

def detalle_documento(request, documento_id):
    """Muestra el detalle de un documento"""
    try:
        documento = Documento.objects.get(id=ObjectId(documento_id))
    except (Documento.DoesNotExist, ValueError):
        messages.error(request, 'Documento no encontrado.')
        return redirect('lista_documentos')
    
    context = {
        'documento': documento,
    }
    
    return render(request, 'mi_aplication/detalle_documento.html', context)

def editar_documento(request, documento_id):
    """Edita un documento existente"""
    try:
        documento = Documento.objects.get(id=ObjectId(documento_id))
    except (Documento.DoesNotExist, ValueError):
        messages.error(request, 'Documento no encontrado.')
        return redirect('lista_documentos')
    
    if request.method == 'POST':
        try:
            # Actualizar datos del formulario
            documento.titulo = request.POST.get('titulo')
            documento.descripcion = request.POST.get('descripcion', '')
            documento.tipo = request.POST.get('tipo')
            documento.url = request.POST.get('url', '')
            documento.formato = request.POST.get('formato', '')
            
            tamaño_str = request.POST.get('tamaño', '0')
            documento.tamaño = int(tamaño_str) if tamaño_str and tamaño_str.strip() else 0
            
            documento.version = request.POST.get('version', '1.0')
            documento.autor = request.POST.get('autor', '')
            documento.palabras_clave = request.POST.get('palabras_clave', '')
            documento.fecha_actualizacion = timezone.now()
            
            documento.save()
            
            messages.success(request, f'Documento "{documento.titulo}" actualizado exitosamente.')
            return redirect('detalle_documento', documento_id=documento.id)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el documento: {str(e)}')
    
    context = {
        'documento': documento,
        'tipos_documento': TIPOS_DOCUMENTO
    }
    
    return render(request, 'mi_aplication/editar_documento.html', context)

def eliminar_documento(request, documento_id):
    """Elimina un documento"""
    try:
        documento = Documento.objects.get(id=ObjectId(documento_id))
    except (Documento.DoesNotExist, ValueError):
        messages.error(request, 'Documento no encontrado.')
        return redirect('lista_documentos')
    
    if request.method == 'POST':
        try:
            titulo = documento.titulo
            documento.delete()
            
            messages.success(request, f'Documento "{titulo}" eliminado exitosamente.')
            return redirect('lista_documentos')
            
        except Exception as e:
            messages.error(request, f'Error al eliminar el documento: {str(e)}')
    
    context = {
        'documento': documento,
    }
    
    return render(request, 'mi_aplication/eliminar_documento.html', context)


def estadisticas_capacitacion_api(request):
    """API para obtener estadísticas de capacitación en formato JSON"""
    try:
        # Por ahora devolvemos datos de ejemplo para mostrar la gráfica
        # TODO: Conectar con datos reales de la base de datos
        
        resultado = {
            'total': 245,
            'categorias': [
                {
                    'codigo': 'DOCENTE',
                    'nombre': 'Docente',
                    'total': 120,
                    'cursos': [
                        {'codigo': 'CIENCIA_DATOS', 'nombre': 'Ciencia de Datos', 'total': 45},
                        {'codigo': 'INTELIGENCIA_ARTIFICIAL', 'nombre': 'Inteligencia Artificial', 'total': 35},
                        {'codigo': 'METODOLOGIA_INVESTIGACION', 'nombre': 'Metodología de Investigación', 'total': 40}
                    ]
                },
                {
                    'codigo': 'ADMINISTRATIVO', 
                    'nombre': 'Administrativo',
                    'total': 65,
                    'cursos': [
                        {'codigo': 'LIDERAZGO', 'nombre': 'Liderazgo', 'total': 30},
                        {'codigo': 'GESTION_PROYECTOS', 'nombre': 'Gestión de Proyectos', 'total': 20},
                        {'codigo': 'RECURSOS_HUMANOS', 'nombre': 'Gestión de Recursos Humanos', 'total': 15}
                    ]
                },
                {
                    'codigo': 'DIRECTIVO',
                    'nombre': 'Directivo', 
                    'total': 35,
                    'cursos': [
                        {'codigo': 'PLANEACION_ESTRATEGICA', 'nombre': 'Planeación Estratégica', 'total': 20},
                        {'codigo': 'CALIDAD_EDUCATIVA', 'nombre': 'Calidad Educativa', 'total': 15}
                    ]
                },
                {
                    'codigo': 'INVESTIGADOR',
                    'nombre': 'Investigador',
                    'total': 25,
                    'cursos': [
                        {'codigo': 'REDACCION_CIENTIFICA', 'nombre': 'Redacción Científica', 'total': 15},
                        {'codigo': 'ESTADISTICA_AVANZADA', 'nombre': 'Estadística Avanzada', 'total': 10}
                    ]
                }
            ],
            'fecha_actualizacion': timezone.now().isoformat()
        }
        
        return JsonResponse(resultado)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'total': 0,
            'categorias': []
        }, status=500)


def dashboard_capacitaciones(request):
    """Dashboard principal con gráfica de flor para capacitaciones"""
    import json
    from collections import defaultdict
    from .constants import CATEGORIAS_FORMATIVAS, CURSOS_ESPECIFICOS
    
    # Estadísticas básicas
    total_participantes = Participante.objects.count()
    
    # Preparar datos para la gráfica de flor
    try:
        # Obtener participantes con categoría formativa
        participantes_con_categoria = Participante.objects.filter(categoria_formativa__exists=True, categoria_formativa__ne='')
        total_capacitados = participantes_con_categoria.count()
        
        # Si no hay datos reales, usar datos de ejemplo basados en CATEGORIAS_FORMATIVAS
        if total_capacitados == 0:
            # Crear datos de ejemplo dinámicamente desde CATEGORIAS_FORMATIVAS
            dict_categorias = dict(CATEGORIAS_FORMATIVAS)
            dict_cursos = dict(CURSOS_ESPECIFICOS)
            
            # Generar datos de ejemplo dinámicamente basados en las categorías disponibles
            # Algunos cursos comunes que podrían aplicar a múltiples categorías
            cursos_comunes = [
                'METODOLOGIA_INVESTIGACION',
                'REDACCION_CIENTIFICA', 
                'ESTADISTICA_AVANZADA',
                'PEDAGOGIA_DIGITAL',
                'METODOLOGIAS_ACTIVAS',
                'EVALUACION_EDUCATIVA',
                'CIENCIA_DATOS',
                'INTELIGENCIA_ARTIFICIAL',
                'DESARROLLO_MOVIL',
                'CLOUD_COMPUTING'
            ]
            
            # Crear datos de ejemplo para cada categoría dinámicamente
            import random
            datos_ejemplo = {}
            
            for codigo_cat, nombre_cat in CATEGORIAS_FORMATIVAS:
                # Asignar un total aleatorio entre 40 y 150
                total_cat = random.randint(40, 150)
                
                # Seleccionar 3-5 cursos aleatoriamente de los disponibles
                num_cursos = random.randint(3, 5)
                cursos_disponibles = [c for c, _ in CURSOS_ESPECIFICOS]
                cursos_seleccionados = random.sample(cursos_disponibles, min(num_cursos, len(cursos_disponibles)))
                
                # Distribuir el total entre los cursos seleccionados
                cursos_lista = []
                total_restante = total_cat
                for i, curso_codigo in enumerate(cursos_seleccionados):
                    if i == len(cursos_seleccionados) - 1:
                        # Último curso toma lo que queda
                        total_curso = total_restante
                    else:
                        # Otros cursos toman una porción aleatoria
                        max_para_este = total_restante - (len(cursos_seleccionados) - i - 1)
                        total_curso = random.randint(10, max(10, max_para_este - 10))
                        total_restante -= total_curso
                    
                    cursos_lista.append((curso_codigo, total_curso))
                
                datos_ejemplo[codigo_cat] = {
                    'total': total_cat,
                    'cursos': cursos_lista
                }
            
            
            categorias_ejemplo = []
            total_ejemplo = 0
            
            for codigo_cat, nombre_cat in CATEGORIAS_FORMATIVAS:
                if codigo_cat in datos_ejemplo:
                    datos_cat = datos_ejemplo[codigo_cat]
                    cursos_lista = []
                    
                    for codigo_curso, total_curso in datos_cat['cursos']:
                        nombre_curso = dict_cursos.get(codigo_curso, codigo_curso)
                        cursos_lista.append({
                            'codigo': codigo_curso,
                            'nombre': nombre_curso,
                            'total': total_curso
                        })
                    
                    categorias_ejemplo.append({
                        'codigo': codigo_cat,
                        'nombre': nombre_cat,
                        'total': datos_cat['total'],
                        'cursos': cursos_lista
                    })
                    total_ejemplo += datos_cat['total']
            
            datos_grafica = {
                'total': total_ejemplo,
                'categorias': categorias_ejemplo
            }
        else:
            # Procesar datos reales de la base de datos
            stats_por_categoria = {}
            
            for participante in participantes_con_categoria:
                if participante.categoria_formativa:
                    categoria = participante.categoria_formativa
                    
                    # Inicializar categoría si no existe
                    if categoria not in stats_por_categoria:
                        stats_por_categoria[categoria] = {
                            'total': 0,
                            'cursos': {}
                        }
                    
                    stats_por_categoria[categoria]['total'] += 1
                    
                    # Contar cursos específicos
                    if hasattr(participante, 'cursos_especificos') and participante.cursos_especificos:
                        for curso in participante.cursos_especificos:
                            if curso not in stats_por_categoria[categoria]['cursos']:
                                stats_por_categoria[categoria]['cursos'][curso] = 0
                            stats_por_categoria[categoria]['cursos'][curso] += 1
            
            # Convertir a formato para la gráfica
            # Usar el orden de CATEGORIAS_FORMATIVAS para consistencia
            categorias_data = []
            dict_categorias = dict(CATEGORIAS_FORMATIVAS)
            dict_cursos = dict(CURSOS_ESPECIFICOS)
            
            # Iterar sobre las categorías en el orden definido en constants.py
            for codigo_categoria, nombre_categoria in CATEGORIAS_FORMATIVAS:
                # SIEMPRE incluir la categoría, incluso si no tiene datos (será 0)
                if codigo_categoria in stats_por_categoria:
                    stats = stats_por_categoria[codigo_categoria]
                    
                    cursos_data = []
                    for codigo_curso, total in stats['cursos'].items():
                        nombre_curso = dict_cursos.get(codigo_curso, codigo_curso)
                        cursos_data.append({
                            'codigo': codigo_curso,
                            'nombre': nombre_curso,
                            'total': total
                        })
                    
                    # Ordenar cursos por total descendente
                    cursos_data.sort(key=lambda x: x['total'], reverse=True)
                    
                    categorias_data.append({
                        'codigo': codigo_categoria,
                        'nombre': nombre_categoria,
                        'total': stats['total'],
                        'cursos': cursos_data
                    })
                else:
                    # Categoría sin datos, agregar con total 0
                    categorias_data.append({
                        'codigo': codigo_categoria,
                        'nombre': nombre_categoria,
                        'total': 0,
                        'cursos': []
                    })
            
            datos_grafica = {
                'total': total_capacitados,
                'categorias': categorias_data
            }
            
    except Exception as e:
        # En caso de error, usar datos de ejemplo
        total_capacitados = 0
        datos_grafica = {
            'total': 245,
            'categorias': [
                {
                    'codigo': 'DOCENTE',
                    'nombre': 'Docente',
                    'total': 120,
                    'cursos': [
                        {'codigo': 'CIENCIA_DATOS', 'nombre': 'Ciencia de Datos', 'total': 45},
                        {'codigo': 'INTELIGENCIA_ARTIFICIAL', 'nombre': 'Inteligencia Artificial', 'total': 35}
                    ]
                },
                {
                    'codigo': 'ADMINISTRATIVO',
                    'nombre': 'Administrativo',
                    'total': 65,
                    'cursos': [
                        {'codigo': 'LIDERAZGO', 'nombre': 'Liderazgo', 'total': 30}
                    ]
                }
            ]
        }
    
    # Reuniones de capacitación
    reuniones_capacitacion = ReunionNacional.objects.filter(
        tipo__in=['CURSO_CAPACITACION', 'TALLER', 'SEMINARIO', 'DIPLOMADO']
    ).count()
    
    # Próximas capacitaciones - las 10 más cercanas a la fecha actual (pasadas o futuras)
    from datetime import datetime
    fecha_actual = datetime.now().date()
    
    capacitaciones = ReunionNacional.objects.filter(
        tipo__in=['CURSO_CAPACITACION', 'TALLER', 'SEMINARIO', 'DIPLOMADO']
    )
    
    # Ordenar por cercanía a la fecha actual
    proximas_capacitaciones = sorted(
        capacitaciones,
        key=lambda r: abs((r.fecha_inicio - fecha_actual).days) if r.fecha_inicio else float('inf')
    )[:10]
    
    context = {
        'total_participantes': total_participantes,
        'total_capacitados': max(total_capacitados, datos_grafica['total']),
        'reuniones_capacitacion': reuniones_capacitacion,
        'proximas_capacitaciones': proximas_capacitaciones,
        'porcentaje_capacitados': round((max(total_capacitados, datos_grafica['total']) / max(total_participantes, 1) * 100), 1),
        'datos_grafica_json': json.dumps(datos_grafica),  # Pasar datos como JSON al template
    }
    
    return render(request, 'mi_aplication/dashboard_capacitaciones.html', context)