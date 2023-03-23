from __future__ import absolute_import
from celery import Celery
import os, ssl

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lmcservice.settings')

app = Celery("lmcservice", broker_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE},
             redis_backend_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE})
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
