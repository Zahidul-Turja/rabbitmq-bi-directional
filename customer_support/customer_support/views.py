from django.http import JsonResponse
from customer_support.events.publisher import event_publisher


def trigger_ticket_event(request):
    """Test endpoint to publish ticket event to ecom"""
    event_publisher.publish(
        task_name="handle_ticket_event",
        routing_key="ticket.created",
        payload={
            "name": "Samsung A50",
        },
        # payload={
        #     "id": 123,
        #     "customer_id": 456,
        #     "subject": "Order delivery issue",
        #     "priority": "high",
        # },
        headers={"source": "customer_support", "version": "1.0"},
    )
    return JsonResponse({"status": "OK", "message": "Ticket event published"})


def trigger_complaint_event(request):
    """Test endpoint to publish complaint event to ecom"""
    event_publisher.publish(
        task_name="handle_complaint_event",
        routing_key="complaint.filed",
        payload={"id": 789, "customer_id": 456, "complaint": "Product quality issue"},
        headers={"source": "customer_support", "version": "1.0"},
    )
    return JsonResponse({"status": "OK", "message": "Complaint event published"})
