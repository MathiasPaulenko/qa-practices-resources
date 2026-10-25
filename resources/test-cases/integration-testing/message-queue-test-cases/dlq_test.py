"""TC-002: message routes to DLQ after exceeding max retries."""
import pika

params = pika.ConnectionParameters('localhost', credentials=pika.PlainCredentials('test', 'test'))
channel = pika.BlockingConnection(params).channel()

channel.exchange_declare(exchange='orders.dlx', exchange_type='fanout')
channel.queue_declare(queue='orders.dlq', durable=True)
channel.queue_bind(queue='orders.dlq', exchange='orders.dlx')

args = {
    'x-dead-letter-exchange': 'orders.dlx',
    'x-message-ttl': 1000,  # message expires unacked -> DLQ (simulates max retries)
}
channel.queue_declare(queue='orders', durable=True, arguments=args)
channel.basic_publish(exchange='', routing_key='orders', body='bad-message')

import time
time.sleep(2)  # let TTL expire
method, _, body = channel.basic_get(queue='orders.dlq', auto_ack=True)
assert body == b'bad-message', body
print('PASS: poison message landed in orders.dlq')
