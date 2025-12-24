from django.http import JsonResponse
from customer_support.events.publisher import event_publisher


def trigger_product_event(request):
    """Test endpoint to publish product event to ecom"""
    event_publisher.publish(
        task_name="handle_product_event",
        routing_key="product.created",
        payload={
            "name": "Samsung A50",
        },
        headers={"source": "customer_support", "version": "1.0"},
    )
    return JsonResponse({"status": "OK", "message": "Ticket event published"})


# def trigger_complaint_event(request):
#     """Test endpoint to publish complaint event to ecom"""
#     event_publisher.publish(
#         task_name="handle_complaint_event",
#         routing_key="complaint.filed",
#         payload={"id": 789, "customer_id": 456, "complaint": "Product quality issue"},
#         headers={"source": "customer_support", "version": "1.0"},
#     )
#     return JsonResponse({"status": "OK", "message": "Complaint event published"})
