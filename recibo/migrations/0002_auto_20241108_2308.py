# Generated by Django 2.1.5 on 2024-11-08 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recibo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
