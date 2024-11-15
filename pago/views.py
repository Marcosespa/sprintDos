from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from cronograma.models import ConceptoPago, Cronograma, CronogramaConcepto
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.exceptions import ValidationError
from datetime import datetime


@login_required
def procesar_pago(request):
    if request.method == 'POST':
        try:
            rate_limit_payment(request.user.id)
            usuario_padre = UsuarioPadreFamilia.objects.get(id=request.user.id)
            concepto_id = request.POST.get('concepto_id')
            valor_pago = request.POST.get('valor_pago')
            
            concepto = get_object_or_404(ConceptoPago, id=concepto_id)
            cronograma = Cronograma.objects.get(
                usuario_padre=usuario_padre,
                mes=concepto.mes_aplicable,
                año_escolar=concepto.año_escolar
            )
            
            cronograma_concepto = CronogramaConcepto.objects.get(
                cronograma=cronograma,
                concepto=concepto
            )
            
            if float(valor_pago) > cronograma_concepto.saldo_pendiente:
                messages.error(request, 'El valor del pago excede el saldo pendiente.')
                return render(request, 'procesar_pago.html')
            
            nuevo_pago = Pago.objects.create(
                nombre_pago=concepto.nombre,
                valor_pago=valor_pago,
                fecha_pago=datetime.now().date(),
                tipo_pago=concepto.tipo,
                estado_pago='PENDIENTE',
                usuario_padre=usuario_padre,
                cronograma=cronograma
            )
            
            # Actualizar saldo pendiente
            cronograma_concepto.saldo_pendiente -= float(valor_pago)
            cronograma_concepto.save()
            
            messages.success(request, 'Pago procesado exitosamente.')
            return redirect('cronograma_index')
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pago: {str(e)}')
            return render(request, 'procesar_pago.html')
    
    # GET request
    conceptos_pendientes = []
    cronogramas = Cronograma.objects.filter(
        usuario_padre=request.user,
        estado__in=['PENDIENTE', 'PARCIAL']
    )
    
    for cronograma in cronogramas:
        for rel in CronogramaConcepto.objects.filter(
            cronograma=cronograma,
            saldo_pendiente__gt=0
        ):
            conceptos_pendientes.append({
                'id': rel.concepto.id,
                'nombre': rel.concepto.nombre,
                'tipo': rel.concepto.get_tipo_display(),
                'saldo': rel.saldo_pendiente,
                'vencimiento': rel.concepto.fecha_vencimiento
            })
    
    return render(request, 'procesar_pago.html', {
        'conceptos_pendientes': conceptos_pendientes
    })


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

def index_PadreFamilia(request):
    return render(request, 'usuarioPadreFamilia/index_PadreFamilia.html')

@login_required
def historial_pagos(request):
    pagos = Pago.objects.filter(usuario_padre=request.user).order_by('-fecha_pago')
    return render(request, 'historial_pagos.html', {'pagos': pagos})


def rate_limit_payment(user_id):
    cache_key = f'payment_attempt_{user_id}'
    attempts = cache.get(cache_key, 0)
    if attempts >= 5:
        raise ValidationError('Demasiados intentos de pago. Por favor, intente más tarde.')
    cache.set(cache_key, attempts + 1, 3600)  # 1 hour expiry


