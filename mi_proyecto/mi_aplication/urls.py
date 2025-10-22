from django.urls import path
from . import views
from . import views_admin

urlpatterns = [
    # URLs del sistema de reuniones nacionales
    path('', views.index, name='index_reuniones'),
    path('reuniones/', views.lista_reuniones, name='lista_reuniones'),
    path('reuniones/crear/', views.crear_reunion, name='crear_reunion'),
    path('reuniones/<str:reunion_id>/', views.detalle_reunion, name='detalle_reunion'),
    path('reuniones/<str:reunion_id>/editar/', views.editar_reunion, name='editar_reunion'),
    path('reuniones/<str:reunion_id>/subir-documento/', views.subir_documento_reunion, name='subir_documento_reunion'),
    path('reuniones/<str:reunion_id>/agregar-participante/', views.agregar_participante_reunion, name='agregar_participante_reunion'),
    path('reuniones/<str:reunion_id>/agregar-participante-existente/', views.agregar_participante_existente_reunion, name='agregar_participante_existente_reunion'),
    
    path('acuerdos/', views.lista_acuerdos, name='lista_acuerdos'),
    path('acuerdos/crear/', views.crear_acuerdo, name='crear_acuerdo'),
    path('acuerdos/<str:acuerdo_id>/', views.detalle_acuerdo, name='detalle_acuerdo'),
    path('acuerdos/<str:acuerdo_id>/editar/', views.editar_acuerdo, name='editar_acuerdo'),
    path('acuerdos/<str:acuerdo_id>/subir-documento/', views.subir_documento_acuerdo, name='subir_documento_acuerdo'),
    
    path('participantes/', views.lista_participantes, name='lista_participantes'),
    path('participantes/crear/', views.crear_participante, name='crear_participante'),
    path('participantes/<str:participante_id>/', views.detalle_participante, name='detalle_participante'),
    path('participantes/<str:participante_id>/editar/', views.editar_participante, name='editar_participante'),
    path('participantes/<str:participante_id>/eliminar/', views.eliminar_participante, name='eliminar_participante'),
    path('documentos/', views.lista_documentos, name='lista_documentos'),
    path('documentos/crear/', views.crear_documento, name='crear_documento'),
    path('documentos/<str:documento_id>/', views.detalle_documento, name='detalle_documento'),
    path('documentos/<str:documento_id>/editar/', views.editar_documento, name='editar_documento'),
    path('documentos/<str:documento_id>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    
    # Rutas adicionales faltantes
    path('reuniones/<str:reunion_id>/eliminar/', views.eliminar_reunion, name='eliminar_reunion'),
    
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('buscar/', views.buscar, name='buscar'),
    
    # Dashboard de capacitaciones
    path('capacitaciones/', views.dashboard_capacitaciones, name='dashboard_capacitaciones'),
    path('api/estadisticas-capacitacion/', views.estadisticas_capacitacion_api, name='api_estadisticas_capacitacion'),
    
    # Administración de constantes
    path('admin/constantes/', views_admin.admin_constantes, name='admin_constantes'),
    path('admin/constantes/editar/<str:categoria>/', views_admin.editar_constante, name='editar_constante'),
    path('admin/constantes/exportar/', views_admin.exportar_constantes, name='exportar_constantes'),
    path('admin/constantes/importar/', views_admin.importar_constantes, name='importar_constantes'),
    path('api/constantes/<str:categoria>/', views_admin.get_constante_api, name='api_constantes'),
]