from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
import asyncio
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 1234
#server_address = ('localhost', port)
server_address = ('192.168.178.157', port)
sock.bind(server_address)

host_name = socket.gethostname()
IPAddress = socket.gethostbyname(host_name)

print("{} @ {}".format(host_name, IPAddress))
print(sock.getsockname())

sock.listen()

	# Waiting for a connection
print('waiting for a connection')
connection, client_address = sock.accept()
print(connection, client_address)

async def consume():
    consumer = AIOKafkaConsumer(
        'my_topic', 'my_other_topic',
        bootstrap_servers='localhost:{}'.format(port),
        group_id="my-group")
    # Get cluster layout and join group `my-group`
    await consumer.start()
    try:
        # Consume messages
        async for msg in consumer:
            print("consumed: ", msg.topic, msg.partition, msg.offset,
                  msg.key, msg.value, msg.timestamp)
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()

asyncio.run(consume())
