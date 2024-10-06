from django.contrib import admin
from django.urls import include, path
from . import views
import usuarioPadreFamilia.urls  # Asegúrate de importar las URLs de tu app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Página principal para el index
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('padre-familia/', include('usuarioPadreFamilia.urls')),  # Incluye las URLs de usuarioPadreFamilia
]