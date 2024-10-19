from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from usuarioPadreFamilia.models import UsuarioPadreFamilia  # Asegúrate que esté bien importado

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        nombre_pago = request.POST.get('nombre_pago')
        valor_pago = request.POST.get('valor_pago')
        fecha_pago = request.POST.get('fecha_pago')
        tipo_pago = request.POST.get('tipo_pago')

        # Crear el nuevo pago
        nuevo_pago = Pago(
            nombre_pago=nombre_pago,
            valor_pago=valor_pago,
            fecha_pago=fecha_pago,
            tipo_pago=tipo_pago,
            estado_pago='PENDIENTE',
        )
        nuevo_pago.save()

        messages.success(request, 'Pago procesado exitosamente.')
        return redirect('index_PadreFamilia')

    return render(request, 'procesar_pago.html')

