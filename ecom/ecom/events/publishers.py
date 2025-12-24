from celery import current_app
import logging

logger = logging.getLogger(__name__)


class EventPublisher:
    """
    Centralized event publisher using Celery's send_task
    """

    def publish(self, task_name, routing_key, payload, headers=None):
        """
        Publish an event to RabbitMQ using Celery

        Args:
            task_name: Name of the Celery task (e.g., 'handle_customer_event')
            routing_key: Routing key (e.g., 'customer.created')
            payload: Dictionary containing event data
            headers: Optional headers dictionary

        Example:
            publisher = EventPublisher()
            publisher.publish(
                'handle_customer_event',
                'customer.created',
                {'name': 'John Doe'}
            )
        """
        try:
            # Prepare the task kwargs
            task_kwargs = {
                "event_type": routing_key,
                "data": payload,
                "headers": headers or {},
            }

            # Send task to the remote worker
            current_app.send_task(
                task_name,
                kwargs=task_kwargs,
                queue=self._get_queue_for_routing_key(routing_key),
                retry=True,
                retry_policy={
                    "interval_start": 0,
                    "interval_step": 2,
                    "interval_max": 30,
                    "max_retries": 5,
                },
            )

            logger.info(f"Published event: {routing_key} to task: {task_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to publish event {routing_key}: {str(e)}")
            raise

    def _get_queue_for_routing_key(self, routing_key):
        """Map routing keys to queues"""
        if routing_key.startswith("customer."):
            return "support_customer_queue"
        elif routing_key.startswith("order."):
            return "support_order_queue"
        elif routing_key.startswith("ticket."):
            return "ecom_ticket_queue"
        elif routing_key.startswith("complaint."):
            return "ecom_complaint_queue"
        return "support_tasks"


# Singleton instance
event_publisher = EventPublisher()
