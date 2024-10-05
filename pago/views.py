# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from .models import Pago
# from django.contrib import messages 
# from django.contrib.auth.models import User

# def pagina_principal(request):
#     if request.user.is_authenticated:
#         return render(request, 'pagina_principal.html') 

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect('pagina_principal') 
#         else:
#             messages.error(request, 'Credenciales incorrectas')

#     return render(request, 'pagina_principal.html')  

# @login_required
# def procesar_pago(request):
#     if request.method == 'POST':
#         valor_pago = request.POST.get('valor_pago')
#         tipo_pago = request.POST.get('tipo_pago')
#         nuevo_pago = Pago(valor_pago=valor_pago, tipo_pago=tipo_pago, estado_pago='PENDIENTE')
#         nuevo_pago.save()
        
#         messages.success(request, 'Pago procesado exitosamente.')
#         return redirect('pagina_principal')  
#     return render(request, 'procesar_pago.html')
# def usuario_padre_familia_edit_view(request):
#     # Lógica de la vista
#     return render(request, 'pago/editar_usuario.html')
# def crear_usuario(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         try:
#             User.objects.create_user(username=username, password=password)
#             messages.success(request, 'Usuario creado con éxito.')
#             return redirect('pagina_principal') 
#         except Exception as e:
#             messages.error(request, f'Error al crear el usuario: {str(e)}')
    
#     return render(request, 'crear_usuario.html')