# Generated by Django 5.1.1 on 2024-10-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronograma', '0002_cronograma_valor'),
        ('usuarioPadreFamilia', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usuariopadrefamilia',
            old_name='user_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='usuariopadrefamilia',
            name='descripcion',
        ),
        migrations.RemoveField(
            model_name='usuariopadrefamilia',
            name='estudiante_relacionado',
        ),
        migrations.RemoveField(
            model_name='usuariopadrefamilia',
            name='valor',
        ),
        migrations.AddField(
            model_name='usuariopadrefamilia',
            name='cronogramas',
            field=models.ManyToManyField(to='cronograma.cronograma'),
        ),
    ]
