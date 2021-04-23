'''
MQTT Client
- Publisher: 센서 데이터를 Edge Node로 전송함
- Subscriber: Edge node가 전송하는 threashold 파라미터들을 수신해서 처리함

'''
import json
import threading
import paho.mqtt.client as mqtt
import time
import sys
BROKER_ADDR = '155.230.120.235'

TOKEN_SENSOR = 'sensors/'
TOKEN_THRESHOLD = 'edge/threshold/'
TOKEN_URG = 'urgent/'

moving_avg_list = list()    # Moving Average를 값을 저장하는 리스트
'''
    MQTT를 이용하여 publish할 data 클래스
    - 센서의 측정 데이터를 JSON 형태로 변환하여 MQTT를 이용하여 전송함 
    JSON dumps() 기능 추가 
'''
class SensorData:
    def __init__(self):
        print('Class of sensor data')
        self.maverage_values = list() # Moving Average List

    def convert_json(self, dev, timestamp, pm25, pm10, temp, humi, priority):
        sensor_data = dict()
        sensor_data['devid'] = dev
        sensor_data['timestamp'] = timestamp
        sensor_data['pm2.5'] = pm25     # 숫자 형태 그대로 저장함
        sensor_data['pm10'] = pm10
        sensor_data['temp'] = temp
        sensor_data['humi'] = humi
        sensor_data['priority'] = priority

        # JSON 형태의 dictionary를 string 형태로 변환함 (json.dumps)
        sensor_data_string = json.dumps(sensor_data)
        #print(sensor_data_string)

        return sensor_data_string
#------------------------------------------------------------------------
'''
    Threshold, Standard deviation, moving average 등을 저장하는 클래스
    JSON Parser 기능 추가   
'''
#------------------------------------------------------------------------
class ThresholdParameters:
    def __init__(self):
        print("Class of Threshold Parameters")

#-------------------------------------------------------------------------
'''
    MQTT Client class
    
'''

class MQTTClient(mqtt.Client):
    def on_connect(self, mqttc, obj, flags, rc):
        if rc == 0:
            print("Connection Ok")
        else:
            print("Connection failed, code= ", rc)

    def on_message(self, mqttc, obj, msg):
        print(msg.topic + " " + str(msg.payload))

    def on_publish(self, mqttc, obj, mid):
        print("on_publish() msg id: " + str(mid))

    def on_subscribe(self, mqttc, obj, mid, qos):
        print("Subscribed: " + str(mid) + " " + str(qos))

    '''
    def on_log(self, mqttc, obj, level, string):
        print(string)
    '''
    def on_disconnect(self, mqttc, flags, rc=0):
        print("Disconnect rc= ", str(rc))

    def convert_json(self, dev, timestamp, pm25, pm10, temp, humi, priority):
        sensor_data = dict()
        sensor_data['devid'] = dev
        sensor_data['timestamp'] = timestamp
        sensor_data['pm2.5'] = pm25  # 숫자 형태 그대로 저장함
        sensor_data['pm10'] = pm10
        sensor_data['temp'] = temp
        sensor_data['humi'] = humi
        sensor_data['priority'] = priority

        # JSON 형태의 dictionary를 string 형태로 변환함 (json.dumps)
        sensor_data_string = json.dumps(sensor_data)
        #print(sensor_data_string)

        return sensor_data_string

    def run_publish(self, token, interval):
        # keepalive = 60
        print("Publish Thread Start")
        self.connect(BROKER_ADDR, 1883, 60)
        self.loop_start()
        count = 1
        while True:
            #--------------------------------------------------------
            # Read sensor data here
            #--------------------------------------------------------

            # devid, timestamp, pm25, pm10, temp, humi, priority
            sensor_string = self.convert_json(1, count, 10, 10, 10, 10, 2)
            self.publish(token, sensor_string, qos=1)
            #print('publish: ', sensor_string)
            time.sleep(interval)
            count += 1
            if (count > 10):
                break

        print("Publishing Stop")
        self.disconnect()

    def thread_publish(self, token, interval):
        print('thread_publish')
        # token = 'sesnor/'
        t = threading.Thread(target=self.run_publish, args=(token, interval, ))
        #t.daemon = True
        t.start()

    def run_subscribe(self, token, interval):
        print("Subscribe Thread Start")
        self.connect(BROKER_ADDR, 1883, 60)
        self.subscribe(token, qos=1)
        self.loop_forever()

    def thread_subscribe(self, token, interval):
        # token = 'threshold/'
        t = threading.Thread(target=self.run_subscribe, args=(token, interval, ))
        #t.daemon = True
        t.start()
#------------------------------------------------------------------------
def mqtt_main():
    '''
        pub_client: Publisher: Sensor node -> Edge node (전송 데이터: 센서 측정값)
        sub_client: Subscriber: Edge node -> Sensor node (전송 데이터: threshold 값)
    :return:
    '''
    #sys.path.insert(0, '/home/pi/python_workspace/')
    print("<< MQTT Client main >>")
    pub_client = MQTTClient()   # Publisher
    pub_client.thread_publish(TOKEN_SENSOR, 1) # working well
    #mqttc.run_publish(TOKEN_SENSOR, 1)     # TOKEN_PUB = 'sensors/'

    sub_client = MQTTClient()   # Subscriber
    sub_client.thread_subscribe(TOKEN_THRESHOLD, 1) # Not working
    #sub_client.run_subscribe(TOKEN_THRESHOLD, 1)  # TOKEN_SUB = 'edge/threashold/'

mqtt_main()
