from django.urls import path
from . import views

urlpatterns = [
    path('', views.cronograma_index, name='cronograma_index'),
    path('concepto/crear/', views.crear_concepto_pago, name='crear_concepto_pago'),
    path('concepto/lista/', views.lista_conceptos, name='lista_conceptos'),
    path('concepto/editar/<int:concepto_id>/', views.editar_concepto, name='editar_concepto'),
    path('pago/agregar/<int:cronograma_id>/', views.agregar_pago, name='agregar_pago'),
    path('gerente/cronogramas/', views.listado_cronogramas, name='listado_cronogramas'),
    #path('procesar-pago/', views.procesar_pago, name='cronograma_procesar_pago'),
]