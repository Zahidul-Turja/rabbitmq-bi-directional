from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name="handle_product_event", bind=True)
def handle_product_event(self, event_type=None, data=None, headers=None, **kwargs):
    """
    Handle product events from customer support

    event_type examples: 'product.created', 'product.resolved', 'product.closed'
    """
    try:
        from product.models import Product

        logger.info(f"Received product event: {event_type}")
        print(f"product EVENT: {event_type}")
        print(f"DATA: {data}")

        if event_type == "product.created":
            # Handle new product creation
            product = Product.objects.create(name=data.get("name"))
            print(f"New product created: {product.id}")
            # You might want to notify the customer, update order status, etc.

        elif event_type == "product.resolved":
            print(f"product resolved: {data.get('id')}")
            # Update related order/customer records

        return {"status": "processed", "event_type": event_type}
    except Exception as e:
        logger.error(f"Error processing product event: {str(e)}")
        raise


# @shared_task(name="handle_complaint_event", bind=True)
# def handle_complaint_event(self, event_type=None, data=None, headers=None, **kwargs):
#     """Handle complaint events from customer support"""
#     try:
#         logger.info(f"Received complaint event: {event_type}")
#         print(f"COMPLAINT EVENT: {event_type}")
#         print(f"DATA: {data}")

#         return {"status": "processed", "event_type": event_type}
#     except Exception as e:
#         logger.error(f"Error processing complaint event: {str(e)}")
#         raise
