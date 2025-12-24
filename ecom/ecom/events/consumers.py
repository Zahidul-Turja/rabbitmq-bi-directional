from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name="handle_ticket_event", bind=True)
def handle_ticket_event(self, event_type=None, data=None, headers=None, **kwargs):
    """
    Handle ticket events from customer support

    event_type examples: 'ticket.created', 'ticket.resolved', 'ticket.closed'
    """
    try:
        from product.models import Product

        logger.info(f"Received ticket event: {event_type}")
        print(f"TICKET EVENT: {event_type}")
        print(f"DATA: {data}")

        if event_type == "ticket.created":
            # Handle new ticket creation
            product = Product.objects.create(name=data.get("name"))
            print(f"New product created: {product.id}")
            # You might want to notify the customer, update order status, etc.

        elif event_type == "ticket.resolved":
            print(f"Ticket resolved: {data.get('id')}")
            # Update related order/customer records

        return {"status": "processed", "event_type": event_type}
    except Exception as e:
        logger.error(f"Error processing ticket event: {str(e)}")
        raise


@shared_task(name="handle_complaint_event", bind=True)
def handle_complaint_event(self, event_type=None, data=None, headers=None, **kwargs):
    """Handle complaint events from customer support"""
    try:
        logger.info(f"Received complaint event: {event_type}")
        print(f"COMPLAINT EVENT: {event_type}")
        print(f"DATA: {data}")

        return {"status": "processed", "event_type": event_type}
    except Exception as e:
        logger.error(f"Error processing complaint event: {str(e)}")
        raise
