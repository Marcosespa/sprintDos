# Generated by Django 3.2.6 on 2024-10-18 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cronograma', '0003_auto_20241018_0406'),
        ('usuarioPadreFamilia', '0003_auto_20241018_0406'),
        ('descuento', '0002_auto_20241018_0406'),
        ('recibo', '0003_auto_20241018_0406'),
        ('pago', '0006_auto_20241018_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pago',
            name='cronograma',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagos_asociados_pago', to='cronograma.cronograma'),
        ),
        migrations.RemoveField(
            model_name='pago',
            name='descuentos',
        ),
        migrations.AddField(
            model_name='pago',
            name='descuentos',
            field=models.ManyToManyField(related_name='pagos_cronograma', to='descuento.Descuento'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='estado_pago',
            field=models.CharField(default='PENDIENTE', max_length=20),
        ),
        migrations.AlterField(
            model_name='pago',
            name='fecha_pago',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='pago',
            name='nombre_pago',
            field=models.CharField(default='Pago genérico', max_length=100),
        ),
        migrations.AlterField(
            model_name='pago',
            name='recibo',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pago_pago', to='recibo.recibo'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='tipo_pago',
            field=models.CharField(default='Pendiente', max_length=100),
        ),
        migrations.AlterField(
            model_name='pago',
            name='usuario_padre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagos_asociados_pago', to='usuarioPadreFamilia.usuariopadrefamilia'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='valor_pago',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]