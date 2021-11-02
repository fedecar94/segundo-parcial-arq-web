from rest_framework.serializers import ModelSerializer

from .models import (Asignacion, Bolsa, Cliente, Concepto, Uso, UsoDetalle,
                     Vencimiento)


class AsignacionSerializer(ModelSerializer):
    class Meta:
        model = Asignacion
        fields = '__all__'


class BolsaSerializer(ModelSerializer):
    class Meta:
        model = Bolsa
        fields = '__all__'


class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
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


class VencimientoSerializer(ModelSerializer):
    class Meta:
        model = Vencimiento
        fields = '__all__'
