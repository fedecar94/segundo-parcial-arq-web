from celery import shared_task
from django.utils import timezone

from puntos.models import Bolsa


@shared_task
def limpiar_saldos_vencidos():
    bolsas = Bolsa.objects.filter(vencimiento__lt=timezone.now())
    bolsas.update(saldo=0)
    print(f'Se limpiaron {bolsas.count()} bolsas')

