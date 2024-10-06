from django.contrib import admin
from django.urls import include, path
from . import views
import usuarioPadreFamilia.urls  # Asegúrate de importar las URLs de tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('',include(usuarioPadreFamilia.urls)),
    

    # path('', pagina_principal, name='pagina_principal'),
    # path('index_PadreFamilia/', include('usuarioPadreFamilia.urls')),
    # path('pago/', include('pago.urls')),
    # path('cronograma/', include('cronograma.urls')),
    
]
