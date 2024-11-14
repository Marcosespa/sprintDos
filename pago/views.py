from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from usuarioPadreFamilia.models import UsuarioPadreFamilia  # Asegúrate que esté bien importado
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail


@login_required
def procesar_pago(request):
    if request.method == 'POST':
        try:
            rate_limit_payment(request.user.id)
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

            enviar_notificacion_pago(nuevo_pago)

            messages.success(request, 'Pago procesado exitosamente.')
            return redirect('index_PadreFamilia')

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('procesar_pago')

    return render(request, 'procesar_pago.html')


def enviar_notificacion_pago(pago):
    subject = f'Nuevo pago registrado: {pago.nombre_pago}'
    message = f'''
    Se ha registrado un nuevo pago:
    Nombre: {pago.nombre_pago}
    Valor: S/. {pago.valor_pago}
    Fecha: {pago.fecha_pago}
    Estado: {pago.estado_pago}
    '''
    send_mail(
        subject,
        message,
        'from@example.com',
        [pago.usuario_padre.email],
        fail_silently=True,
    )


@login_required
def historial_pagos(request):
    pagos = Pago.objects.filter(usuario_padre=request.user).order_by('-fecha_pago')
    return render(request, 'historial_pagos.html', {'pagos': pagos})


