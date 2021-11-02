import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "segundo_parcial_arq_web.settings")

app = Celery("config")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'limpiar-bolsas-cada-hora': {
        'task': 'puntos.tasks.limpiar_saldos_vencidos',
        'schedule': 60 * 60  # 60 segundos por 60 minutos
    },
}


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
