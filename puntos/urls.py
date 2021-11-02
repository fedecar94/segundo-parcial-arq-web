"""puntos URL Configuration"""
from rest_framework.routers import DefaultRouter

from .views import (AsignacionViewSet, BolsaViewSet, ClienteViewSet,
                    ConceptoViewSet, UsoViewSet, VencimientoViewSet)

router = DefaultRouter()

router.register('asignacion', AsignacionViewSet)
router.register('bolsa', BolsaViewSet)
router.register('cliente', ClienteViewSet)
router.register('concepto', ConceptoViewSet)
router.register('uso', UsoViewSet)
router.register('vencimiento', VencimientoViewSet)

urlpatterns = router.urls
