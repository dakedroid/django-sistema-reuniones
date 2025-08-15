from django.urls import path
from . import views

urlpatterns = [
    # URLs del sistema de reuniones nacionales
    path('test/', views.test_view, name='test_view'),
    path('test-page/', views.test_page, name='test_page'),
    path('', views.index, name='index_reuniones'),
    path('reuniones/', views.lista_reuniones, name='lista_reuniones'),
    path('reuniones/crear/', views.crear_reunion, name='crear_reunion'),
    path('reuniones/<str:reunion_id>/', views.detalle_reunion, name='detalle_reunion'),
    path('reuniones/<str:reunion_id>/editar/', views.editar_reunion, name='editar_reunion'),
    path('reuniones/<str:reunion_id>/subir-documento/', views.subir_documento_reunion, name='subir_documento_reunion'),
    path('reuniones/<str:reunion_id>/agregar-participante/', views.agregar_participante_reunion, name='agregar_participante_reunion'),
    path('reuniones/<str:reunion_id>/agregar-participante-existente/', views.agregar_participante_existente_reunion, name='agregar_participante_existente_reunion'),
    
    path('acuerdos/', views.lista_acuerdos, name='lista_acuerdos'),
    path('acuerdos/<str:acuerdo_id>/', views.detalle_acuerdo, name='detalle_acuerdo'),
    path('acuerdos/<str:acuerdo_id>/subir-documento/', views.subir_documento_acuerdo, name='subir_documento_acuerdo'),
    
    path('participantes/', views.lista_participantes, name='lista_participantes'),
    path('participantes/crear/', views.crear_participante, name='crear_participante'),
    path('participantes/<str:participante_id>/', views.detalle_participante, name='detalle_participante'),
    path('participantes/<str:participante_id>/editar/', views.editar_participante, name='editar_participante'),
    path('participantes/<str:participante_id>/eliminar/', views.eliminar_participante, name='eliminar_participante'),
    path('documentos/', views.lista_documentos, name='lista_documentos'),
    
    path('estadisticas/', views.estadisticas, name='estadisticas'),
    path('buscar/', views.buscar, name='buscar'),
]