from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Pago
from usuarioPadreFamilia.models import UsuarioPadreFamilia  # Asegúrate que esté bien importado
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.cache import cache
from django.core.exceptions import ValidationError


@login_required
def procesar_pago(request):
    if request.method == 'POST':
        try:
            rate_limit_payment(request.user.id)
            usuario_padre = request.user
            nombre_pago = request.POST.get('nombre_pago')
            valor_pago = request.POST.get('valor_pago')
            fecha_pago = request.POST.get('fecha_pago')
            tipo_pago = request.POST.get('tipo_pago')

            # Detailed validation with specific error messages
            if not nombre_pago:
                messages.error(request, 'El nombre del pago es requerido.')
                return render(request, 'procesar_pago.html')
            if not valor_pago:
                messages.error(request, 'El valor del pago es requerido.')
                return render(request, 'procesar_pago.html')
            if not fecha_pago:
                messages.error(request, 'La fecha del pago es requerida.')
                return render(request, 'procesar_pago.html')
            if not tipo_pago:
                messages.error(request, 'El tipo de pago es requerido.')
                return render(request, 'procesar_pago.html')

            try:
                valor_pago = float(valor_pago)
                if valor_pago <= 0:
                    messages.error(request, 'El valor del pago debe ser mayor a 0.')
                    return render(request, 'procesar_pago.html')
            except ValueError:
                messages.error(request, 'El valor del pago debe ser un número válido.')
                return render(request, 'procesar_pago.html')

            nuevo_pago = Pago(
                nombre_pago=nombre_pago,
                valor_pago=valor_pago,
                fecha_pago=fecha_pago,
                tipo_pago=tipo_pago,
                estado_pago='PENDIENTE',
                usuario_padre=usuario_padre
            )

            # Debug information
            print(f"Datos del pago a crear:")
            print(f"Nombre: {nombre_pago}")
            print(f"Valor: {valor_pago}")
            print(f"Fecha: {fecha_pago}")
            print(f"Tipo: {tipo_pago}")
            print(f"Usuario: {usuario_padre.username}")
            
            nuevo_pago.save()
            
            # Verify the save and send notification
            if nuevo_pago.pk:
                try:
                    enviar_notificacion_pago(nuevo_pago)
                except Exception as e:
                    print(f"Error al enviar notificación: {str(e)}")
                    # Continue even if notification fails
                
                messages.success(request, 'Pago procesado exitosamente.')
                return redirect('index_PadreFamilia')
            else:
                messages.error(request, 'Error al guardar el pago.')
                return render(request, 'procesar_pago.html')
                
        except ValidationError as e:
            print(f"ValidationError: {str(e)}")
            messages.error(request, str(e))
            return render(request, 'procesar_pago.html')
        except Exception as e:
            print(f"Error inesperado: {type(e).__name__} - {str(e)}")
            messages.error(request, 'Error al procesar el pago. Por favor intente nuevamente.')
            return render(request, 'procesar_pago.html')
    
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


