import math
from datetime import timedelta
from math import floor

from django.db import transaction
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import (Asignacion, Bolsa, Cliente, Concepto, Uso, UsoDetalle,
                     Vencimiento)
from .serializers import (AsignacionSerializer, BolsaSerializer,
                          ClienteSerializer, ConceptoSerializer, UsoSerializer,
                          VencimientoSerializer, CalularPuntosSerializer)


class AsignacionViewSet(ModelViewSet):
    queryset = Asignacion.objects.all()
    serializer_class = AsignacionSerializer


class BolsaViewSet(GenericViewSet, ListModelMixin):
    queryset = Bolsa.objects.all()
    serializer_class = BolsaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            bolsa = serializer.save()

            venc = Vencimiento.objects.filter(inicio_validez__lte=timezone.now(), fin_validez__gte=timezone.now()).first()
            bolsa.vencimiento = bolsa.asignacion + timedelta(days=venc.duracion)

            asig = Asignacion.objects.filter(limite_inferior__lte=bolsa.monto, limite_superior__gte=bolsa.monto).first()
            if not asig:
                asig = Asignacion.objects.filter(limite_inferior=0, limite_superior=0).first()
            bolsa.p_asignado = floor(bolsa.monto / asig.equivalencia)

            bolsa.save()
        return Response(self.get_serializer(bolsa).data, status=201)


class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer


class ConceptoViewSet(ModelViewSet):
    queryset = Concepto.objects.all()
    serializer_class = ConceptoSerializer


class UsoViewSet(GenericViewSet, ListModelMixin):
    queryset = Uso.objects.all()
    serializer_class = UsoSerializer

    def get_serializer_class(self):
        if self.action == 'calcular':
            return CalularPuntosSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            uso = serializer.save()
            now = timezone.now()
            puntos = uso.p_utilizado
            while puntos > 0:
                bolsa = uso.cliente.bolsas.filter(vencimiento__gte=now, saldo__gt=0).order_by('asignacion').first()
                menor = puntos if puntos < bolsa.saldo else bolsa.saldo
                bolsa.p_utilizado += menor
                bolsa.save()
                UsoDetalle.objects.create(
                    uso=uso,
                    p_utilizado=menor,
                    bolsa=bolsa
                )
                puntos -= menor
        return Response(self.get_serializer(uso).data, status=201)

    @action(methods=['post'], detail=False)
    def calcular(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        monto = serializer.data.get('monto')

        asignacion = Asignacion.objects.filter(limite_inferior__lte=monto, limite_superior__gte=monto).first()
        if not asignacion:
            asignacion = Asignacion.objects.get(limite_inferior=0, limite_superior=0)

        equivale = math.floor(monto/asignacion.equivalencia)
        return Response({'monto': monto, 'equivale': equivale}, status=200)


class VencimientoViewSet(ModelViewSet):
    queryset = Vencimiento.objects.all()
    serializer_class = VencimientoSerializer
