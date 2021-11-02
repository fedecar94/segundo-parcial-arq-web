from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    CEDULA_PARAGUAYA = 'CIP'
    PASAPORTE = 'PAS'
    TIPOS_DE_DOCUMENTO_CHOICES = [
        (CEDULA_PARAGUAYA, 'Cedula paraguaya'),
        (PASAPORTE, 'Pasaporte'),
    ]

    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    nro_documento = models.CharField(max_length=32)
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DE_DOCUMENTO_CHOICES, default=CEDULA_PARAGUAYA)
    nacionalidad = models.CharField(max_length=2, default='PY')
    email = models.EmailField()
    telefono = models.CharField(max_length=32, blank=True)
    fecha_nacimiento = models.DateField(blank=True)

    def __str__(self):
        return f"{self.tipo_documento} {self.nro_documento} - {self.nombres} {self.apellidos}"


class Concepto(models.Model):
    descripcion = models.CharField(max_length=255)
    puntos_requerido = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.descripcion


class Asignacion(models.Model):
    limite_inferior = models.PositiveIntegerField(default=0)
    limite_superior = models.PositiveIntegerField(default=0)
    equivalencia = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.limite_inferior} Gs. a {self.limite_superior} Gs. 1 punto cada {self.equivalencia}"


class Vencimiento(models.Model):
    inicio_validez = models.DateTimeField()
    fin_validez = models.DateTimeField()
    duracion = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.inicio_validez} al {self.fin_validez} duran {self.duracion} dias"


class Bolsa(models.Model):
    cliente = models.ForeignKey('puntos.Cliente', on_delete=models.CASCADE, related_name='bolsas')
    asignacion = models.DateTimeField(auto_now_add=True)
    vencimiento = models.DateTimeField(default=timezone.now(), editable=False)
    p_asignado = models.PositiveIntegerField(default=0, editable=False)
    p_utilizado = models.PositiveIntegerField(default=0, editable=False)
    saldo = models.PositiveIntegerField(default=0, editable=False)
    monto = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.cliente} {self.asignacion} {self.saldo}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.saldo = self.p_asignado - self.p_utilizado
        super().save(force_insert, force_update, using, update_fields)


class Uso(models.Model):
    cliente = models.ForeignKey('puntos.Cliente', on_delete=models.CASCADE, related_name='usos')
    p_utilizado = models.PositiveIntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    concepto = models.ForeignKey('puntos.Concepto', on_delete=models.CASCADE, related_name='usos')

    def __str__(self):
        return f"{self.fecha} {self.cliente}"


class UsoDetalle(models.Model):
    uso = models.ForeignKey('puntos.Uso', on_delete=models.CASCADE, related_name='detalles')
    p_utilizado = models.PositiveIntegerField(default=0)
    bolsa = models.ForeignKey('puntos.Bolsa', on_delete=models.CASCADE, related_name='detalles_uso')

    def __str__(self):
        return f"Uso: {self.uso} Bolsa.id: {self.bolsa.id}"
