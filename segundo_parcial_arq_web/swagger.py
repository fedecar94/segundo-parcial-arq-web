
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Gestor de puntos",
        default_version="v1",
        description="Endpoints para el frontend",
        contact=openapi.Contact(email="fedecar94@fpuna.edu.py"),
        license=openapi.License(name="GPL-3.0 License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
