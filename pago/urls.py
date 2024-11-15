from django.urls import path

from usuarioPadreFamilia.views import index_PadreFamilia
from . import views
from .views import crear_usuario, pagina_principal, procesar_pago, usuario_padre_familia_edit_view  

urlpatterns = [
    
    
    path('', pagina_principal, name='pagina_principal'), 
    path('procesar_pago/', procesar_pago, name='procesar_pago'), 
    path('editar_usuario/', usuario_padre_familia_edit_view, name='editar_usuario'),
    path('health-check/', views.healthCheck, name='health_check'),
    #path('crear-usuario/', crear_usuario, name='crear_usuario'),
    #path('index_PadreFamilia/', index_PadreFamilia, name='index_PadreFamilia'),
    path('usuarioPadreFamilia/index_PadreFamilia/', views.index_PadreFamilia, name='index_PadreFamilia'),

]
