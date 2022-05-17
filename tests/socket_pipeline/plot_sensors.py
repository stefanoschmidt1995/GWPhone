"""
This build a very simple pipeline for handling a streaming set of accelerometric data from the phone.
It's done in a very unelegant way with custom defined classes

"""
import socket
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button

#####################

class plot_manager():
	
	def init_plot(self, dt):
		self.dt = dt
		self.fig, self.ax = plt.subplots(figsize=(12,12))
		#plt.subplots_adjust(left=0.25, bottom=0.25)
		self.lab = ['x','y','z']
		self.l_list = [self.ax.plot(np.zeros((1,)), np.zeros((1,)), '-', ms=1, label = self.lab[i])[0] for i in range(3)]
		self.ax.legend(loc = 'upper right')
		self.ax.set_xlabel("Time (s)")
		self.ax.set_ylim([-25, 25])

	def update_plot(self, plotdata, t):
		t_list = np.linspace(-plotdata.shape[0]*self.dt, 0, plotdata.shape[0])+t
		for i, l in enumerate(self.l_list):
			l.set_xdata(t_list)
			l.set_ydata(plotdata[:,i])

		self.ax.set_xlim([np.min(t_list), np.max(t_list) + (np.max(t_list) - np.min(t_list))*0.1])
		self.ax.set_ylim([min(-15, np.min(plotdata)), max(15, np.max(plotdata))])
		self.fig.canvas.draw_idle()
		
		plt.pause(0.01)
		
		return

#####################
	#Initializing some variables
dt = 0.06
accelerometer_data = np.zeros((int(10/dt),3))
data_list = [] #list with raw data
rot_list = [] #list with rotational data
t = 0

plt_manager = plot_manager()

	
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server_address = ('192.168.178.157', 1234)
server_address = ('192.168.1.102', 1234)
sock.bind(server_address)

sock.listen()

	# Waiting for a connection
print('waiting for a connection')
connection, client_address = sock.accept()
print(connection, client_address)

plt_manager.init_plot(dt)

while True:
	data, ancdata, msg_flags, address = connection.recvmsg(1000000)
	try:
		data = eval(data)
	except SyntaxError:
		continue
	
		#STEP 1: getting the data and putting them in a fixed length buffer (and putting them on an uniform grid)
		#FIXME: times here are all fucked up: you should take care of that...
		#FIXME: things are sooo slower than before!! Whyyyy?
	print(data)
	data_list.append(data['accelerometer'])
	rot_list.append(data['rotationVector'])
	new_times_ = np.array([d['timestamp'] for d in data_list])/1e9
	new_data_ = np.array([d['value'] for d in data_list])
	rot_vec_data_ = np.array([d['value'] for d in rot_list])
	
	t = t+dt*len(new_data_)

	accelerometer_data = np.roll(accelerometer_data, -len(new_data_), axis = 0)
	accelerometer_data[-len(new_data_):,:] = new_data_
	
	data_list = []


		#STEP 2: upload plot
	plt_manager.update_plot(accelerometer_data, t)


		#STEP 3: compute the GW strain (only on the new data)...
	



















