from django.db.models import Sum
from django.utils import timezone

from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, ValidationError

from .models import (Asignacion, Bolsa, Cliente, Concepto, Uso, UsoDetalle,
                     Vencimiento)


class AsignacionSerializer(ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'


class BolsaSerializer(ModelSerializer):
    cliente = ClienteSerializer()

    class Meta:
        model = Bolsa
        fields = '__all__'


class ConceptoSerializer(ModelSerializer):
    class Meta:
        model = Concepto
        fields = '__all__'


class UsoDetalleSerializer(ModelSerializer):
    bolsa = BolsaSerializer()

    class Meta:
        model = UsoDetalle
        fields = '__all__'


class UsoSerializer(ModelSerializer):
    detalles = UsoDetalleSerializer(many=True, read_only=True)

    class Meta:
        model = Uso
        fields = '__all__'

    def validate(self, attrs):
        concepto = attrs.get('concepto')
        p_utilizado = attrs.get('p_utilizado')
        cliente = attrs.get('cliente')

        if p_utilizado < concepto.puntos_requerido:
            raise ValidationError({
                'p_utilizado': 'No son suficientes puntos para el concepto'
            })

        if p_utilizado > cliente.bolsas.filter(vencimiento__gte=timezone.now(), saldo__gt=0).aggregate(total=Sum('saldo'))['total']:
            raise ValidationError({
                'p_utilizado': 'El cliente no posee suficientes puntos'
            })

        return attrs


class CalularPuntosSerializer(Serializer):
    monto = IntegerField(default=0)
    equivale = IntegerField(read_only=True)


class VencimientoSerializer(ModelSerializer):
    class Meta:
        model = Vencimiento
        fields = '__all__'
