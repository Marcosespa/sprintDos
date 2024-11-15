from django import forms
from .models import Pago
from django.utils import timezone

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['nombre_pago', 'valor_pago', 'fecha_pago', 'tipo_pago']
        
    def clean_valor_pago(self):
        valor = self.cleaned_data['valor_pago']
        if valor <= 0:
            raise forms.ValidationError('El valor del pago debe ser mayor a 0')
        return valor 

    def clean_fecha_pago(self):
        fecha_pago = self.cleaned_data['fecha_pago']
        today = timezone.now().date()
        if fecha_pago > today:
            raise forms.ValidationError('La fecha de pago no puede ser una fecha futura')
        return fecha_pago

    # Optional: Add custom widgets or styles if needed
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['nombre_pago'].widget.attrs.update({'class': 'custom-class'})
