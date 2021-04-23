import paho.mqtt.client as mqtt
import json
import time

loop_flag = 1
def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("connected Ok")
	else:
		print("Bad connection Returned code= ", rc)

def on_disconnect(client, userdata, flags, rc=0):
	print(str(rc))

def on_publish(client, userdata, mid):
	print("In on_pub callback mid: ", mid)

def json_string(devid, timestamp, pm25, pm10, temp, humi, priority):
	sensor_data = dict()
	sensor_data['devid'] = devid
	sensor_data['timestamp'] = timestamp
	sensor_data['pm2.5'] = pm25
	sensor_data['pm10'] = pm10
	sensor_data['temp'] = temp
	sensor_data['humi'] = humi
	sensor_data['priority'] = priority
	
	sensor_data_string = json.dumps(sensor_data)
	print(sensor_data_string)
	return sensor_data_string

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

client.connect('155.230.120.235', 1883)
client.loop_start()
count = 0
sensor_string = ""
dev_id = 5
while loop_flag==1:
	# devid, timestamp, pm25, pm10, temp, humi, priority
	sensor_string = json_string(dev_id, count, 50, 50, 50, 50, 2) 
	client.publish('sensing_value', sensor_string, qos=1)
	time.sleep(1)
	count +=1
	if(count > 10):
		break

print("Publish stop");
client.loop_stop()
client.disconnect()

