from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ReunionNacional, Acuerdo, Participante, Documento
from .models import ParticipanteEmbebido, DocumentoEmbebido, AgendaEmbebido, SeguimientoEmbebido
from django.utils import timezone

def test_view(request):
    """Vista de prueba para verificar que todo funcione"""
    try:
        # Probar que podemos acceder a los modelos
        reuniones = ReunionNacional.objects.all()
        acuerdos = Acuerdo.objects.all()
        participantes = Participante.objects.all()
        documentos = Documento.objects.all()
        
        context = {
            'reuniones_count': reuniones.count(),
            'acuerdos_count': acuerdos.count(),
            'participantes_count': participantes.count(),
            'documentos_count': documentos.count(),
            'status': 'OK'
        }
        
        return JsonResponse(context)
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 'ERROR'})

def test_page(request):
    """Página de prueba para verificar funcionalidades"""
    return render(request, 'mi_aplication/test.html')

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
    
    # Reuniones próximas
    reuniones_proximas = ReunionNacional.objects.filter(
        estado__in=['PLANIFICADA', 'EN_CURSO']
    ).order_by('fecha_inicio')[:5]
    
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
        try:
            from datetime import datetime
            
            # Obtener datos del formulario
            titulo = request.POST.get('titulo')
            tipo = request.POST.get('tipo')
            estado = request.POST.get('estado')
            fecha_inicio = datetime.fromisoformat(request.POST.get('fecha_inicio').replace('T', ' '))
            fecha_fin = datetime.fromisoformat(request.POST.get('fecha_fin').replace('T', ' '))
            sede = request.POST.get('sede')
            descripcion = request.POST.get('descripcion')
            objetivos = request.POST.get('objetivos')
            organizador_principal = request.POST.get('organizador_principal') or None
            participantes_esperados = int(request.POST.get('participantes_esperados', 0))
            presupuesto_asignado = float(request.POST.get('presupuesto_asignado', 0)) if request.POST.get('presupuesto_asignado') else None
            modalidad = request.POST.get('modalidad', 'PRESENCIAL')
            enlace_videollamada = request.POST.get('enlace_videollamada') or None
            direccion_fisica = request.POST.get('direccion_fisica') or None
            
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
        'tipos_reunion': ReunionNacional.TIPOS_REUNION,
        'estados': ReunionNacional.ESTADOS,
        'modalidades': ReunionNacional.MODALIDADES,
    }
    
    return render(request, 'mi_aplication/crear_reunion.html', context)

def editar_reunion(request, reunion_id):
    """Edita una reunión existente"""
    try:
        from bson import ObjectId
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            from datetime import datetime
            
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
        from bson import ObjectId
        reunion = ReunionNacional.objects.get(id=ObjectId(reunion_id))
    except (ReunionNacional.DoesNotExist, ValueError):
        messages.error(request, 'Reunión no encontrada.')
        return redirect('lista_reuniones')
    
    if request.method == 'POST':
        try:
            # Crear documento embebido
            documento = DocumentoEmbebido(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                tipo=request.POST.get('tipo'),
                url=request.POST.get('url', ''),
                formato=request.POST.get('formato', ''),
                tamaño=int(request.POST.get('tamaño', 0)),
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
        'tipos_documento': [
            ('AGENDA', 'Agenda'),
            ('ACTA', 'Acta'),
            ('PRESENTACION', 'Presentación'),
            ('MEMORANDUM', 'Memorándum'),
            ('CIRCULAR', 'Circular'),
            ('OTRO', 'Otro'),
        ]
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
        'tipos_participante': [
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('INVITADO', 'Invitado'),
        ]
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
                    instituto=participante.instituto,
                    departamento=participante.departamento,
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
            documento = DocumentoEmbebido(
                titulo=request.POST.get('titulo'),
                descripcion=request.POST.get('descripcion', ''),
                tipo=request.POST.get('tipo'),
                url=request.POST.get('url', ''),
                formato=request.POST.get('formato', ''),
                tamaño=int(request.POST.get('tamaño', 0)),
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
        'tipos_documento': [
            ('AGENDA', 'Agenda'),
            ('ACTA', 'Acta'),
            ('PRESENTACION', 'Presentación'),
            ('MEMORANDUM', 'Memorándum'),
            ('CIRCULAR', 'Circular'),
            ('OTRO', 'Otro'),
        ]
    }
    
    return render(request, 'mi_aplication/subir_documento_acuerdo.html', context)

def lista_participantes(request):
    """Lista todos los participantes"""
    participantes = Participante.objects.all().order_by('apellido_paterno', 'nombre')
    
    # Filtros
    tipo = request.GET.get('tipo')
    confirmado = request.GET.get('confirmado')
    instituto = request.GET.get('instituto')
    
    if tipo:
        participantes = participantes.filter(tipo_participante=tipo)
    if confirmado:
        participantes = participantes.filter(confirmado=confirmado == 'true')
    if instituto:
        participantes = participantes.filter(instituto__icontains=instituto)
    
    # Convertir a lista para paginación
    participantes_list = list(participantes)
    
    # Paginación manual
    paginator = Paginator(participantes_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipos_participante': [
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('INVITADO', 'Invitado'),
        ]
    }
    
    return render(request, 'mi_aplication/lista_participantes.html', context)

def crear_participante(request):
    """Crea un nuevo participante"""
    if request.method == 'POST':
        try:
            # Crear participante
            participante = Participante(
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
            participante.save()
            
            messages.success(request, f'Participante "{participante.nombre} {participante.apellido_paterno}" creado exitosamente.')
            return redirect('lista_participantes')
            
        except Exception as e:
            messages.error(request, f'Error al crear el participante: {str(e)}')
    
    context = {
        'tipos_participante': [
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('INVITADO', 'Invitado'),
        ]
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
            # Actualizar datos del participante
            participante.nombre = request.POST.get('nombre')
            participante.apellido_paterno = request.POST.get('apellido_paterno')
            participante.apellido_materno = request.POST.get('apellido_materno', '')
            participante.email = request.POST.get('email')
            participante.telefono = request.POST.get('telefono', '')
            participante.instituto = request.POST.get('instituto')
            participante.departamento = request.POST.get('departamento', '')
            participante.tipo_participante = request.POST.get('tipo_participante')
            participante.confirmado = request.POST.get('confirmado') == 'on'
            participante.observaciones = request.POST.get('observaciones', '')
            
            participante.save()
            
            messages.success(request, f'Participante "{participante.nombre} {participante.apellido_paterno}" actualizado exitosamente.')
            return redirect('lista_participantes')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el participante: {str(e)}')
    
    context = {
        'participante': participante,
        'tipos_participante': [
            ('DIRECTOR', 'Director'),
            ('SUBDIRECTOR', 'Subdirector'),
            ('COORDINADOR', 'Coordinador'),
            ('DOCENTE', 'Docente'),
            ('ADMINISTRATIVO', 'Administrativo'),
            ('INVITADO', 'Invitado'),
        ]
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
        'tipos_documento': [
            ('AGENDA', 'Agenda'),
            ('ACTA', 'Acta'),
            ('PRESENTACION', 'Presentación'),
            ('MEMORANDUM', 'Memorándum'),
            ('CIRCULAR', 'Circular'),
            ('OTRO', 'Otro'),
        ]
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
    tipos_participante = [
        ('DIRECTOR', 'Director'),
        ('SUBDIRECTOR', 'Subdirector'),
        ('COORDINADOR', 'Coordinador'),
        ('DOCENTE', 'Docente'),
        ('ADMINISTRATIVO', 'Administrativo'),
        ('INVITADO', 'Invitado'),
    ]
    for tipo in tipos_participante:
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
    tipos_documento = [
        ('AGENDA', 'Agenda'),
        ('ACTA', 'Acta'),
        ('PRESENTACION', 'Presentación'),
        ('MEMORANDUM', 'Memorándum'),
        ('CIRCULAR', 'Circular'),
    ]
    for tipo in tipos_documento:
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
            Q(instituto__icontains=query)
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