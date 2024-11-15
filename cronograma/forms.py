from django import forms
from .models import ConceptoPago

class ConceptoPagoForm(forms.ModelForm):
    MESES_CHOICES = [
        ('ENERO', 'Enero'),
        ('FEBRERO', 'Febrero'),
        ('MARZO', 'Marzo'),
        ('ABRIL', 'Abril'),
        ('MAYO', 'Mayo'),
        ('JUNIO', 'Junio'),
        ('JULIO', 'Julio'),
        ('AGOSTO', 'Agosto'),
        ('SEPTIEMBRE', 'Septiembre'),
        ('OCTUBRE', 'Octubre'),
        ('NOVIEMBRE', 'Noviembre'),
        ('DICIEMBRE', 'Diciembre'),
    ]

    mes_aplicable = forms.ChoiceField(choices=MESES_CHOICES)
    año_escolar = forms.IntegerField(min_value=2024, max_value=2030)
    
    class Meta:
        model = ConceptoPago
        fields = ['nombre', 'tipo', 'valor', 'mes_aplicable', 
                 'año_escolar', 'descripcion', 'fecha_vencimiento']
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
