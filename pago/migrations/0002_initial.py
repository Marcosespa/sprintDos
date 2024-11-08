# Generated by Django 4.2.16 on 2024-10-19 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarioPadreFamilia', '0001_initial'),
        ('pago', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pago',
            name='usuario_padre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pagos_asociados_pago', to='usuarioPadreFamilia.usuariopadrefamilia'),
        ),
    ]