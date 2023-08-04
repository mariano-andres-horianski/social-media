// A script to consume RabbitMQ messages sent by the backend

const amqp = require('amqplib/callback_api');

async function consumeMessages() {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    const queue = 'my_queue';
  
    await channel.assertQueue(queue);
  
    channel.consume(queue, (msg) => {
      const message = msg.content.toString();
      console.log('Received message:', message);
      // Process the message or update your UI
    }, { noAck: true });
  }
  
  consumeMessages();