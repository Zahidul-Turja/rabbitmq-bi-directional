import os
from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customer_support.settings")

app = Celery("customer_support")
app.config_from_object("django.conf:settings", namespace="CELERY")

# Define exchanges
customer_exchange = Exchange("customer_events", type="topic", durable=True)

# Define queues customer support consumes from
app.conf.task_queues = (
    # Queue("support_tasks", routing_key="support.#"),
    Queue(
        "support_customer_queue",
        customer_exchange,
        routing_key="customer.*",
        durable=True,
    ),
)

app.conf.accept_content = ["json", "application/json"]
app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.task_ignore_result = False

app.autodiscover_tasks()

from customer_support.events.consumers import (
    handle_customer_event,
)  # noqa
