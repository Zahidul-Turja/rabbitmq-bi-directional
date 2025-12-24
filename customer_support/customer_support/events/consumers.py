from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name="handle_customer_event", bind=True)
def handle_customer_event(self, event_type=None, data=None, headers=None, **kwargs):
    """Handle customer events from ecom service"""
    try:
        logger.info(f"Received customer event: {event_type}")
        print(f"CUSTOMER EVENT: {event_type}")
        print(f"DATA: {data}")

        if event_type == "customer.created":
            # Do something with the customer data
            print(f"New customer created: {data.get('name')}")

        return {"status": "processed", "event_type": event_type}
    except Exception as e:
        logger.error(f"Error processing customer event: {str(e)}")
        raise


# @shared_task(name="handle_order_event", bind=True)
# def handle_order_event(self, event_type=None, data=None, headers=None, **kwargs):
#     """Handle order events from ecom service"""
#     try:
#         logger.info(f"Received order event: {event_type}")
#         print(f"ORDER EVENT: {event_type}")

#         return {"status": "processed", "event_type": event_type}
#     except Exception as e:
#         logger.error(f"Error processing order event: {str(e)}")
#         raise
