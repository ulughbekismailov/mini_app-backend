import os
from celery import Celery

# Django settings modulini sozlash
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Django settings dan Celery sozlamalarini o'qish (CELERY_ prefiksli)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Barcha Django app'laridagi tasks.py fayllarini avtomatik topish
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')