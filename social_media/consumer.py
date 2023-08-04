import pika
from social_media.models import Post

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a queue for the messages
channel.queue_declare(queue='posts')

def on_message(ch, method, properties, body):
    post_data = json.loads(body)

    post = Post(
        owner=post_data['owner'],
        image=post_data['image'],
        likes=post_data['likes'],
        created_at=post_data['created_at'],
        updated_at=post_data['updated_at'],
        caption=post_data['caption'],
    )

    # Save the Post object to the database
    post.save()

# Start listening for messages on the queue
channel.basic_consume(on_message, queue='posts', no_ack=True)

# Start the loop that will keep listening for messages
channel.start_consuming()

# Close the connection to the RabbitMQ server
connection.close()