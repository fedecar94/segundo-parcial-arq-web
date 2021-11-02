# Generated by Django 3.2.9 on 2021-11-02 12:41

import datetime

import django.db.models.deletion
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limite_inferior', models.PositiveIntegerField(default=0)),
                ('limite_superior', models.PositiveIntegerField(default=0)),
                ('equivalencia', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bolsa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asignacion', models.DateTimeField(auto_now_add=True)),
                ('vencimiento', models.DateTimeField(default=datetime.datetime(2021, 11, 2, 12, 41, 9, 414658, tzinfo=utc), editable=False)),
                ('p_asignado', models.PositiveIntegerField(default=0, editable=False)),
                ('p_utilizado', models.PositiveIntegerField(default=0, editable=False)),
                ('saldo', models.PositiveIntegerField(default=0, editable=False)),
                ('monto', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('nro_documento', models.CharField(max_length=32)),
                ('tipo_documento', models.CharField(choices=[('CIP', 'Cedula paraguaya'), ('PAS', 'Pasaporte')], default='CIP', max_length=3)),
                ('nacionalidad', models.CharField(default='PY', max_length=2)),
                ('email', models.EmailField(max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=32)),
                ('fecha_nacimiento', models.DateField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Concepto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('puntos_requerido', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Uso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_utilizado', models.PositiveIntegerField(default=0)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usos', to='puntos.cliente')),
                ('concepto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usos', to='puntos.concepto')),
            ],
        ),
        migrations.CreateModel(
            name='Vencimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inicio_validez', models.DateTimeField()),
                ('fin_validez', models.DateTimeField()),
                ('duracion', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UsoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_utilizado', models.PositiveIntegerField(default=0)),
                ('bolsa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles_uso', to='puntos.bolsa')),
                ('uso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='puntos.uso')),
            ],
        ),
        migrations.AddField(
            model_name='bolsa',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bolsas', to='puntos.cliente'),
        ),
    ]