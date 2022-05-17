#https://towardsdatascience.com/make-a-mock-real-time-stream-of-data-with-python-and-kafka-7e5e23123582

import socket
from kafka import KafkaProducer

class AccelerometerProducer(KafkaProducer):
	
	def __init__(self, hostname, port, **kwargs):
		super().__init__(**kwargs)
		self.server_address = (hostname, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect(self.server_address)
			print("Connected to server")
		except ConnectionRefusedError:
			raise ConnectionRefusedError("Unable to connect to the streaming accelerometer source @ {}:{}. Make sure the server is working".format(hostname, port))
	
	def send(self, topic = 'accelerometer', **kwargs):
		data = self.s.recv(10000000)
		print("Sending: ", data)
		super().send('accelerometer', data, **kwargs)
	
	def stream_data(self, N_iteration = None):
		i = 0
	
		while True:
			self.send()
			i +=1
			if isinstance(N_iteration, int):
				if i>=N_iteration: break
		return
	
#####################################

hostname = '192.168.178.24'
port = 1234

	#Creating the kafka producer
producer = AccelerometerProducer(hostname, port, bootstrap_servers='localhost:9092', api_version = (2,0,0), acks = 0)

producer.stream_data()













