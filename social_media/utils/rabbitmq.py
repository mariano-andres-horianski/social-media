import pika
import json
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def publish_message(queue_name, message):
    try:
        parameters = pika.URLParameters(settings.RABBITMQ_URL)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        
        # Ensure the queue exists
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Publish message
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )
        
        connection.close()
        logger.info(f"Published message to {queue_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to publish message: {str(e)}")
        return False