# views.py en sprintDos
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usuarioPadreFamilia.models import UsuarioPadreFamilia

@login_required
def index(request):
    
    return render(request, 'index_PadreFamilia.html')

    # if request.user.is_authenticated:
    #     return render(request, 'index.html')  # Plantilla para usuarios autenticados

    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     try:
    #         user = UsuarioPadreFamilia.objects.get(username=username)
    #         if user.check_password(password):
    #             login(request, user) 
    #             return redirect('index_PadreFamilia') 
    #         else:
    #             messages.error(request, 'Credenciales incorrectas')
    #             return redirect('index')  
    #     except UsuarioPadreFamilia.DoesNotExist:
    #         messages.error(request, 'Credenciales incorrectas')
    #         return redirect('index')  

    # return render(request, 'index_PadreFamilia.html')

def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if UsuarioPadreFamilia.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            try:
                usuario = UsuarioPadreFamilia(username=username)
                usuario.set_password(password)  # Establece la contraseña de forma segura
                usuario.save()
                messages.success(request, 'Usuario creado con éxito.')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Error al crear el usuario: {str(e)}')

    return render(request, 'crear_usuario.html')
  
@login_required
def index_PadreFamilia(request):
    return render(request, 'index_PadreFamilia.html')
