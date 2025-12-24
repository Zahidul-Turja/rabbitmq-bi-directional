from django.http import JsonResponse
from .events.publishers import event_publisher


def trigger(request):
    event_type = "customer.created"
    event_publisher.publish(
        task_name="handle_customer_event",  # The Celery task name
        routing_key=event_type,
        payload={"from": "E-Commerce"},
        headers={"source": "ecom", "version": "1.0"},
    )
    return JsonResponse({"status": "OK", "message": "E commerce"})
