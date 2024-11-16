from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages  
from cronograma.forms import ConceptoPagoForm
from pago.forms import PagoForm
from usuarioPadreFamilia.models import UsuarioPadreFamilia
from cronograma.models import Cronograma, ConceptoPago, CronogramaConcepto
from pago.models import Pago
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from sprintDos.auth0backend import getRole

def es_gerente(user):
    return user.groups.filter(name='Gerente').exists()

def es_padre_de_familia(user):
    return user.groups.filter(name='Padre De Familia').exists()

def listado_cronogramas(request):
    cronogramas = Cronograma.objects.all()
    pagos = Pago.objects.all()

    # Construir un diccionario de pagos asociados a cada cronograma
    pagos_dict = {}
    for pago in pagos:
        if pago.cronograma_id not in pagos_dict:
            pagos_dict[pago.cronograma_id] = []
        pagos_dict[pago.cronograma_id].append(pago)

    # Pasar el diccionario a la plantilla
    return render(request, 'listado_cronogramas.html', {'cronogramas': cronogramas, 'pagos': pagos_dict})

# Vista de índice de cronograma
@login_required
@user_passes_test(es_padre_de_familia)
def cronograma_index(request):
    if not isinstance(request.user, UsuarioPadreFamilia):
        messages.error(request, 'Acceso no autorizado.')
        return redirect('index_PadreFamilia')
        
    año_actual = datetime.now().year
    cronogramas = Cronograma.objects.filter(
        usuario_padre=request.user,
        año_escolar=año_actual
    ).prefetch_related('conceptos')
    
    resumen_pagos = []
    for cronograma in cronogramas:
        conceptos_detalle = []
        for rel in CronogramaConcepto.objects.filter(cronograma=cronograma):
            conceptos_detalle.append({
                'nombre': rel.concepto.nombre,
                'valor_original': rel.concepto.valor,
                'saldo_pendiente': rel.saldo_pendiente,
                'fecha_vencimiento': rel.concepto.fecha_vencimiento
            })
        
        resumen_pagos.append({
            'mes': cronograma.mes,
            'conceptos': conceptos_detalle,
            'total_pendiente': cronograma.saldo_pendiente,
            'estado': cronograma.estado
        })
    
    return render(request, 'cronograma_index.html', {
        'resumen_pagos': resumen_pagos
    })

# Vista para agregar un nuevo pago
@login_required
@csrf_exempt
def agregar_pago(request, cronograma_id):
    cronograma = get_object_or_404(Cronograma, id=cronograma_id)

    if request.method == 'POST':
        form = PagoForm(request.POST)  
        if form.is_valid():
            pago = form.save(commit=False)
            pago.cronograma = cronograma
            pago.usuario_padre = request.user
            pago.save()  # Guardar el pago

            # Actualizar el saldo pendiente del cronograma
            cronograma.saldo_pendiente = cronograma.valor_total - sum(
                p.valor_pago for p in cronograma.pagos_asociados.filter(estado_pago='COMPLETADO')
            )
            cronograma.save()

            messages.success(request, 'Pago agregado exitosamente.')
            return redirect('cronograma_index')
    else:
        form = PagoForm()

    return render(request, 'agregar_pago.html', {'form': form, 'cronograma': cronograma})

@login_required
@user_passes_test(es_gerente)
def crear_concepto_pago(request):
    if request.method == 'POST':
        form = ConceptoPagoForm(request.POST)
        if form.is_valid():
            concepto = form.save(commit=False)
            concepto.creado_por = request.user
            concepto.save()
            
            # Crear cronogramas para todos los padres
            padres = UsuarioPadreFamilia.objects.all()
            for padre in padres:
                cronograma, created = Cronograma.objects.get_or_create(
                    año_escolar=concepto.año_escolar,
                    mes=concepto.mes_aplicable,
                    usuario_padre=padre,
                    defaults={'estado': 'PENDIENTE'}
                )
                CronogramaConcepto.objects.create(
                    cronograma=cronograma,
                    concepto=concepto,
                    saldo_pendiente=concepto.valor
                )
            
            messages.success(request, 'Concepto de pago creado exitosamente')
            return redirect('lista_conceptos')
    else:
        form = ConceptoPagoForm()
    
    return render(request, 'cronograma/crear_concepto.html', {'form': form})

@login_required
@user_passes_test(es_gerente)
def lista_conceptos(request):
    año_actual = datetime.now().year
    conceptos = ConceptoPago.objects.filter(año_escolar=año_actual).order_by('mes_aplicable')
    
    # Agrupar conceptos por mes
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
        form = ConceptoPagoForm(request.POST, instance=concepto)
        if form.is_valid():
            concepto = form.save()
            
            # Actualizar saldos pendientes en cronogramas existentes
            cronograma_conceptos = CronogramaConcepto.objects.filter(concepto=concepto)
            for cc in cronograma_conceptos:
                pagos_realizados = sum(
                    p.valor_pago for p in cc.cronograma.pagos.filter(estado_pago='PAGADO')
                )
                cc.saldo_pendiente = concepto.valor - pagos_realizados
                cc.save()
            
            messages.success(request, 'Concepto actualizado exitosamente')
            return redirect('lista_conceptos')
    else:
        form = ConceptoPagoForm(instance=concepto)
    
    return render(request, 'cronograma/editar_concepto.html', {
        'form': form,
        'concepto': concepto
    })

@login_required
@user_passes_test(es_padre_de_familia)
def procesar_pago(request):
    print("Iniciando procesar_pago")  # Mensaje de depuración
    try:
        role = getRole(request)
        print(f"Role obtenido: {role}")  # Mensaje de depuración
        
        if role not in ["Padre de Familia", "Gerente"]:
            messages.error(request, 'Acceso no autorizado.')
            return redirect('index_PadreFamilia')
        
        try:
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
            
            if not conceptos_pendientes:
                messages.info(request, 'No hay pagos pendientes.')
                return redirect('index_PadreFamilia')
            
            print(f"Conceptos pendientes encontrados: {len(conceptos_pendientes)}")  # Mensaje de depuración
            return render(request, 'procesar_pago.html', {
                'conceptos_pendientes': conceptos_pendientes,
                'today': datetime.now().date()
            })
            
        except Exception as e:
            messages.error(request, f'Error al procesar el pago: {str(e)}')
            return redirect('index_PadreFamilia')
    except Exception as e:
        messages.error(request, f'Error al obtener el rol: {str(e)}')
        return redirect('index_PadreFamilia')