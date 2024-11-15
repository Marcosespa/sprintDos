from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import FormularioPago, FormularioConceptoPago
from usuarios.models import UsuarioPadre
from cronogramas.models import Cronograma, ConceptoPago, ConceptoCronograma
from pagos.models import Pago

def es_gerente(usuario):
    return usuario.groups.filter(name='Gerente').exists()

# Vista principal del cronograma
@login_required
def indice_cronograma(request):
    if not isinstance(request.user, UsuarioPadre):
        messages.error(request, 'Acceso no autorizado.')
        return redirect('inicio_padre')

    año_actual = timezone.now().year
    cronogramas = Cronograma.objects.filter(
        usuario_padre=request.user,
        año_escolar=año_actual
    ).select_related('usuario_padre').prefetch_related('conceptos')

    resumen_pagos = []
    for cronograma in cronogramas:
        detalles_conceptos = []
        for relacion in ConceptoCronograma.objects.filter(cronograma=cronograma):
            detalles_conceptos.append({
                'nombre': relacion.concepto.nombre,
                'valor_original': relacion.concepto.valor,
                'saldo_pendiente': relacion.saldo_pendiente,
                'fecha_vencimiento': relacion.concepto.fecha_vencimiento
            })

        resumen_pagos.append({
            'mes': cronograma.mes,
            'conceptos': detalles_conceptos,
            'total_pendiente': cronograma.saldo_pendiente,
            'estado': cronograma.estado
        })

    return render(request, 'cronograma/indice.html', {
        'resumen_pagos': resumen_pagos
    })

# Vista para agregar un pago nuevo
@login_required
@csrf_exempt
def agregar_pago(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id)

    if request.method == 'POST':
        form = FormularioPago(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.cronograma = cronograma
            pago.usuario_padre = request.user
            pago.save()

            messages.success(request, 'Pago registrado con éxito.')
            return redirect('indice_cronograma')
    else:
        form = FormularioPago()

    return render(request, 'pagos/agregar.html', {'form': form, 'cronograma': cronograma})

@login_required
@user_passes_test(es_gerente)
def crear_concepto_pago(request):
    if request.method == 'POST':
        form = FormularioConceptoPago(request.POST)
        if form.is_valid():
            concepto = form.save(commit=False)
            concepto.creado_por = request.user
            concepto.save()
            
            # Crear cronogramas para todos los padres
            padres = UsuarioPadre.objects.all()
            for padre in padres:
                cronograma, created = Cronograma.objects.get_or_create(
                    año_escolar=concepto.año_escolar,
                    mes=concepto.mes_aplicable,
                    usuario_padre=padre,
                    defaults={'estado': 'PENDIENTE'}
                )
                ConceptoCronograma.objects.create(
                    cronograma=cronograma,
                    concepto=concepto,
                    saldo_pendiente=concepto.valor
                )
            
            messages.success(request, 'Concepto de pago creado exitosamente.')
            return redirect('lista_conceptos')
    else:
        form = FormularioConceptoPago()
    
    return render(request, 'cronograma/crear_concepto.html', {'form': form})

@login_required
@user_passes_test(es_gerente)
def lista_conceptos(request):
    año_actual = timezone.now().year
    conceptos = ConceptoPago.objects.filter(año_escolar=año_actual).order_by('mes_aplicable')
    
    conceptos_por_mes = {}
    for concepto in conceptos:
        if concepto.mes_aplicable not in conceptos_por_mes:
            conceptos_por_mes[concepto.mes_aplicable] = []
        conceptos_por_mes[concepto.mes_aplicable].append(concepto)
    
    return render(request, 'cronograma/lista_conceptos.html', {
        'conceptos_por_mes': conceptos_por_mes,
        'año_actual': año_actual
    })

@login_required
@user_passes_test(es_gerente)
def editar_concepto(request, concepto_id):
    concepto = get_object_or_404(ConceptoPago, id=concepto_id)
    
    if request.method == 'POST':
        form = FormularioConceptoPago(request.POST, instance=concepto)
        if form.is_valid():
            concepto = form.save()
            
            cronograma_conceptos = ConceptoCronograma.objects.filter(concepto=concepto)
            for cc in cronograma_conceptos:
                pagos_realizados = sum(
                    pago.valor for pago in cc.cronograma.pagos.filter(estado='PAGADO')
                )
                cc.saldo_pendiente = concepto.valor - pagos_realizados
                cc.save()
            
            messages.success(request, 'Concepto actualizado con éxito.')
            return redirect('lista_conceptos')
    else:
        form = FormularioConceptoPago(instance=concepto)
    
    return render(request, 'cronograma/editar_concepto.html', {
        'form': form,
        'concepto': concepto
    })
