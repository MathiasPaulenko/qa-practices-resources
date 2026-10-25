"""TC-001: RabbitMQ preserves ordering with a single consumer."""
import pika

params = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('test', 'test'))
channel = pika.BlockingConnection(params).channel()
channel.queue_declare(queue='orders', durable=True)

for i in range(100):
    channel.basic_publish(exchange='', routing_key='orders', body=str(i))

received = []
def callback(ch, method, properties, body):
    received.append(int(body))
    if len(received) == 100:
        channel.stop_consuming()

channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
assert received == list(range(100)), received[:10]
print('PASS: 100 messages received in publish order')
