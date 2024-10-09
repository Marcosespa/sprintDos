# views.py en sprintDos
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from django.contrib.auth.models import User  # Importar el modelo de usuario predeterminado de Django
from django.views.decorators.csrf import csrf_protect


@login_required
#@csrf_protect  # No estoy seguro
def index(request):
    
    return render(request, 'index_PadreFamilia.html')



def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificar si el nombre de usuario ya existe en alguna de las dos tablas
        if UsuarioPadreFamilia.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            try:
                # Crear usuario en UsuarioPadreFamilia
                usuario_padre = UsuarioPadreFamilia(username=username)
                usuario_padre.set_password(password)  # Establecer la contraseña de manera segura
                usuario_padre.is_superuser = True  # Hacer al usuario un superusuario
                usuario_padre.is_staff = True  # Permitir acceso a la administración
                usuario_padre.is_active = True  # Asegurar que el usuario esté activo
                usuario_padre.save()

                # Crear usuario también en la tabla auth.User
                user = User(username=username)
                user.set_password(password)  # Establecer la contraseña
                user.is_superuser = True  # Hacer al usuario superusuario en auth.User
                user.is_staff = True  # Permitir acceso al admin
                user.is_active = True  # Asegurar que el usuario esté activo
                user.save()

                messages.success(request, 'Usuario creado con éxito en ambas tablas.')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    return render(request, 'crear_usuario.html')
  
@login_required
def index_PadreFamilia(request):
    return render(request, 'index_PadreFamilia.html')
