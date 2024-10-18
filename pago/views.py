from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Pago
from descuento.models import Descuento  # Importamos el modelo de Descuento
from django.contrib import messages

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        valor_pago = request.POST.get('valor_pago')
        tipo_pago = request.POST.get('tipo_pago')
        nombre_pago = request.POST.get('nombre_pago', 'Pago genérico')
        cronograma_id = request.POST.get('cronograma')
        usuario_padre_id = request.POST.get('usuario_padre')
        recibo_id = request.POST.get('recibo')
        descuentos_ids = request.POST.getlist('descuentos')  # Obtenemos la lista de IDs de descuentos

        # Validar que los campos obligatorios no estén vacíos
        if not valor_pago or not tipo_pago:
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
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
            nombre_pago=nombre_pago,
            estado_pago='PENDIENTE'
        )

        # Asignar relaciones opcionales
        if cronograma_id:
            from cronograma.models import Cronograma
            try:
                cronograma = Cronograma.objects.get(id=cronograma_id)
                nuevo_pago.cronograma = cronograma
            except Cronograma.DoesNotExist:
                messages.error(request, 'El cronograma no existe.')
                return redirect('procesar_pago')

        if usuario_padre_id:
            from usuarioPadreFamilia.models import UsuarioPadreFamilia
            try:
                usuario_padre = UsuarioPadreFamilia.objects.get(id=usuario_padre_id)
                nuevo_pago.usuario_padre = usuario_padre
            except UsuarioPadreFamilia.DoesNotExist:
                messages.error(request, 'El usuario padre no existe.')
                return redirect('procesar_pago')

        if recibo_id:
            from recibo.models import Recibo
            try:
                recibo = Recibo.objects.get(id=recibo_id)
                nuevo_pago.recibo = recibo
            except Recibo.DoesNotExist:
                messages.error(request, 'El recibo no existe.')
                return redirect('procesar_pago')

        # Guardar el pago en la base de datos primero, porque necesitamos una instancia de Pago antes de agregar descuentos
        nuevo_pago.save()

        # Asignar los descuentos seleccionados
        if descuentos_ids:
            try:
                descuentos = Descuento.objects.filter(id__in=descuentos_ids)
                nuevo_pago.descuentos.set(descuentos)  # Asignar la lista de descuentos
            except Descuento.DoesNotExist:
                messages.error(request, 'Uno o más descuentos no existen.')
                return redirect('procesar_pago')

        # Mostrar mensaje de éxito
        messages.success(request, 'El pago ha sido procesado exitosamente.')
        return redirect('procesar_pago')

    # Si el método no es POST, simplemente mostrar el formulario
    return render(request, 'pago/procesar_pago.html')
