# customer_support/management/commands/consume_events.py
from django.core.management.base import BaseCommand
from kombu import Connection, Exchange, Queue
from kombu.exceptions import OperationalError
import logging
import json
import socket

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Consume events from RabbitMQ"

    def handle(self, *args, **options):
        from django.conf import settings

        broker_url = settings.CELERY_BROKER_URL

        # Define exchanges
        customer_exchange = Exchange("customer_events", type="topic", durable=True)
        order_exchange = Exchange("order_events", type="topic", durable=True)

        # Define queues
        customer_queue = Queue(
            "support_customer_queue",
            customer_exchange,
            routing_key="customer.*",
            durable=True,
        )

        order_queue = Queue(
            "support_order_queue", order_exchange, routing_key="order.*", durable=True
        )

        def process_customer_event(body, message):
            """Process customer events"""
            try:
                self.stdout.write(self.style.SUCCESS(f"\n✅ CUSTOMER EVENT RECEIVED"))
                self.stdout.write(f'Event Type: {body.get("event_type")}')
                self.stdout.write(f'Data: {json.dumps(body.get("data"), indent=2)}')
                self.stdout.write(
                    f'Headers: {json.dumps(body.get("headers"), indent=2)}'
                )

                # Add your business logic here
                # Example: Save to database, send notifications, etc.

                message.ack()

            except Exception as e:
                logger.error(f"Error processing customer event: {e}")
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
                message.requeue()

        def process_order_event(body, message):
            """Process order events"""
            try:
                self.stdout.write(self.style.SUCCESS(f"\n✅ ORDER EVENT RECEIVED"))
                self.stdout.write(f'Event Type: {body.get("event_type")}')
                self.stdout.write(f'Data: {json.dumps(body.get("data"), indent=2)}')

                message.ack()

            except Exception as e:
                logger.error(f"Error processing order event: {e}")
                self.stdout.write(self.style.ERROR(f"Error: {e}"))
                message.requeue()

        # Start consuming with proper error handling
        while True:
            try:
                with Connection(broker_url) as conn:
                    with conn.Consumer(
                        queues=[customer_queue, order_queue],
                        callbacks=[process_customer_event, process_order_event],
                        accept=["json"],
                    ) as consumer:
                        self.stdout.write(
                            self.style.SUCCESS(
                                "🚀 Started consuming events from RabbitMQ..."
                            )
                        )
                        self.stdout.write("Listening for:")
                        self.stdout.write(
                            "  - customer.* events on support_customer_queue"
                        )
                        self.stdout.write("  - order.* events on support_order_queue")
                        self.stdout.write("\nPress Ctrl+C to stop\n")

                        while True:
                            try:
                                conn.drain_events(timeout=1)
                            except socket.timeout:
                                # This is normal - no messages available
                                continue
                            except KeyboardInterrupt:
                                self.stdout.write(
                                    self.style.WARNING("\n\nStopping consumer...")
                                )
                                return

            except OperationalError as e:
                logger.error(f"Connection error: {e}")
                self.stdout.write(
                    self.style.ERROR(f"Connection lost. Reconnecting in 5 seconds...")
                )
                import time

                time.sleep(5)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING("\n\nStopping consumer..."))
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                self.stdout.write(
                    self.style.ERROR(f"Error: {e}. Restarting in 5 seconds...")
                )
                import time

                time.sleep(5)
