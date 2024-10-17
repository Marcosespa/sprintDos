from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Pago
from django.contrib import messages 
from django.contrib.auth.models import User

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        valor_pago = request.POST.get('valor_pago')
        tipo_pago = request.POST.get('tipo_pago')
        
        # Validar que los campos no estén vacíos
        if not valor_pago or not tipo_pago:
            messages.error(request, 'Por favor, completa todos los campos.')
            return redirect('procesar_pago')

        try:
            valor_pago = float(valor_pago) 
        except ValueError:
            messages.error(request, 'El valor del pago debe ser un número válido.')
            return redirect('procesar_pago')

        # Crear el nuevo pago
        nuevo_pago = Pago(
            valor_pago=valor_pago, 
            tipo_pago=tipo_pago, 
            estado_pago='PENDIENTE',
            usuario_padre=request.user  # Asociar el pago con el usuario actual
        )
        nuevo_pago.save()
        
        messages.success(request, 'Pago procesado exitosamente.')
        return redirect('usuarioPadreFamilia/index_PadreFamilia')
    
    return render(request, 'procesar_pago.html')
