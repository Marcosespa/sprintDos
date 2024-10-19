from django import forms
from .models import Pago
#dededede
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'id_pago',
            'fecha_pago',
            'valor_pago',
            'estado_pago',
            'tipo_pago',
            'nombre_pago',
            'descuentos',
            'recibo',
            'cronograma',
            'usuario_padre',
        ]

        labels = {
            'id_pago': 'ID del Pago',
            'fecha_pago': 'Fecha del Pago',
            'valor_pago': 'Valor del Pago',
            'estado_pago': 'Estado del Pago',
            'tipo_pago': 'Tipo de Pago',
            'nombre_pago': 'Nombre del Pago',
            'descuentos': 'Descuentos',
            'recibo': 'Recibo',
            'cronograma': 'Cronograma',
            'usuario_padre': 'Usuario Padre',
        }

        widgets = {
            'fecha_pago': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'valor_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado_pago': forms.Select(attrs={'class': 'form-control'}),
            'tipo_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_pago': forms.TextInput(attrs={'class': 'form-control'}),
            'descuentos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'recibo': forms.Select(attrs={'class': 'form-control'}),
            'cronograma': forms.Select(attrs={'class': 'form-control'}),
            'usuario_padre': forms.Select(attrs={'class': 'form-control'}),
        }
