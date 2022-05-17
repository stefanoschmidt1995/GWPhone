#https://towardsdatascience.com/make-a-mock-real-time-stream-of-data-with-python-and-kafka-7e5e23123582

import socket
from kafka import KafkaProducer
import sys
import argparse

class AccelerometerProducer(KafkaProducer):
	
	def __init__(self, hostname, port, **kwargs):
		super().__init__(**kwargs)
		self.server_address = (hostname, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect(self.server_address)
			print("Connected to server {}:{}".format(hostname, port))
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



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description ='Kafka producer that gathers streaming sensor data from a phone TCP server')
	  
	# Adding Arguments
	parser.add_argument('--hostname',type = str, default = '192.168.178.24:1234',
		                help ='Hostname of the server in the format hostname:port (e.g. 192.167.0.1:1234)')

	args, _ = parser.parse_known_args()

	try:
		hostname, port = args.hostname.split(':')[:2]
		port = int(port)
	except:
		raise ValueError("Something went wrong in parsing the hostname")

		#Creating the kafka producer
	producer = AccelerometerProducer(hostname, port, bootstrap_servers='localhost:9092', api_version = (2,0,0), acks = 0)

	producer.stream_data()













