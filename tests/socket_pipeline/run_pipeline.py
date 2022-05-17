import pipeline


hostname = '192.168.178.24'
port = 1234

	#Creating the kafka producer
producer = pipeline.Accelerometer(hostname, port)

tranformation_list = [pipeline.plot_transformation]

p = pipeline.pipeline(tranformation_list, producer(), 3)

p.run()
