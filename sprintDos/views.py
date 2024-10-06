from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.models import User


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')  # Plantilla para usuarios autenticados

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(f"Usuario {username} ha iniciado sesión correctamente.")  # Mensaje en la consola

        if user is not None:
            login(request, user)
            #print(f"Usuario {username} ha iniciado sesión correctamente.")  # Mensaje en la consola
            messages.success(request, 'Usuario creado con éxito.')
            return redirect('/index_PadreFamilia')  # Redirige a 'index_PadreFamilia' si el login es correcto
        else:
            messages.error(request, 'Credenciales incorrectas')

    return render(request, 'index.html')  # Plantilla para login cuando el usuario no está autenticado

def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            try:
                User.objects.create_user(username=username, password=password)
                messages.success(request, 'Usuario creado con éxito.')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    return render(request, 'crear_usuario.html')
