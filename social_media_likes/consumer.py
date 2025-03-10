import pika
import json
import os
import time
import logging
from threading import Thread

logger = logging.getLogger(__name__)

class RabbitMQConsumer(Thread):
    def __init__(self, callback, queue_name, rabbitmq_url=None):
        Thread.__init__(self)
        self.callback = callback
        self.queue_name = queue_name
        self.rabbitmq_url = rabbitmq_url or os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')
        self.daemon = True
        
    def run(self):
        while True:
            try:
                parameters = pika.URLParameters(self.rabbitmq_url)
                connection = pika.BlockingConnection(parameters)
                channel = connection.channel()
                
                channel.queue_declare(queue=self.queue_name, durable=True)
                
                def process_message(ch, method, properties, body):
                    try:
                        message = json.loads(body)
                        self.callback(message)
                        ch.basic_ack(delivery_tag=method.delivery_tag)
                    except Exception as e:
                        logger.error(f"Error processing message: {str(e)}")
                        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
                
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=self.queue_name, on_message_callback=process_message)
                
                logger.info(f"Starting consumer for queue: {self.queue_name}")
                channel.start_consuming()
            except Exception as e:
                logger.error(f"Consumer error: {str(e)}")
                time.sleep(5)  # Wait before reconnecting