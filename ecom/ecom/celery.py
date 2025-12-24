import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ecom.settings")

app = Celery("ecom")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Define exchanges
product_exchange = Exchange("product_events", type="topic", durable=True)
complaint_exchange = Exchange("complaint_events", type="topic", durable=True)

# Define queues that ecom consumes from
app.conf.task_queues = (
    Queue(
        "ecom_product_queue",
        product_exchange,
        routing_key="product.*",
        durable=True,
    ),
    Queue(
        "ecom_complaint_queue",
        complaint_exchange,
        routing_key="complaint.*",
        durable=True,
    ),
)

app.conf.accept_content = ["json", "application/json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.task_ignore_result = False

app.autodiscover_tasks()

from ecom.events.consumers import handle_product_event
