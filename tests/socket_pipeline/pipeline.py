"""
Some class creating abstractions to build a pipeline that takes data from the phone and do shit
"""

import socket
import json

class Accelerometer():
	
	def __init__(self, hostname, port):
		self.server_address = (hostname, port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect(self.server_address)
			print("Connected to server")
		except ConnectionRefusedError:
			raise ConnectionRefusedError("Unable to connect to the streaming accelerometer source @ {}:{}. Make sure the server is working".format(hostname, port))
		self.buffer = []
	
	def __call__(self):
		#FIXME: this should be async!! We don't want to wait to receive data to do stuff
		while True:
			data = self.s.recv(10000000)
			data = data.decode('utf8').replace("'", '"')
			data = data.split('\n')[:-1]
			#print("Accelerometer: ",data)
			self.buffer.extend(data)

			while True: #checking for errors
				to_return = self.buffer.pop(0)
				try:
					to_return = json.loads(to_return)
					break
				except:
					pass
			print(len(self.buffer), to_return)
			
			yield to_return
		return

class pipeline():
	def __init__(self, transformation_list, generator, len_buffer = 1):
			#building the pipeline
		self.pipeline_chain = generator
		for t in transformation_list:
			self.pipeline_chain = t(self.pipeline_chain)
		return
	
	def run(self):
		for _ in self.pipeline_chain:
			pass

class transformation():
	
	def __init__(self, input_generator, len_buffer = 1):
		self.buffer = [] #buffer of inputs
		self.max_len = len_buffer
		self.input_generator = input_generator
	
	def transform(self, input_buffer):
		raise NotImplementedError("This must be implemented in subclasses")
	
	def __iter__(self):
		for x in self.input_generator:
			self.buffer.append(x)
			if len(self.buffer)>self.max_len:
				self.buffer.pop(0)
			yield self.transform(self.buffer)


class plot_transformation(transformation):
	def transform(self, input_buffer):
		#print("plot_transformation: ", input_buffer)
		return input_buffer


