from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['nombre_pago', 'valor_pago', 'fecha_pago', 'tipo_pago']
        
    def clean_valor_pago(self):
        valor = self.cleaned_data['valor_pago']
        if valor <= 0:
            raise forms.ValidationError('El valor del pago debe ser mayor a 0')
        return valor 