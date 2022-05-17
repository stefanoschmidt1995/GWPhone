from kafka import KafkaConsumer
import json

# utiliser kafka
consumer = KafkaConsumer('accelerometer', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', 
			api_version='2.0.0', enable_auto_commit=True)# group_id="accelerometer_id", value_deserializer = json.loads)
print('before for ')
for msg in consumer:
	print('IN for')
	#print(type(consumer))
	print(msg)
	#print(json.loads(msg.value.decode()))

print("DIOMERDA")
