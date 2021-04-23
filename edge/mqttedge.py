'''
    MQTT Edge Client
        - Publisher: Threshold 파라미터 값들을 IoT node들에게 전송함
        - Subscriber: IoT node들이 전송하는 sensor 측정값을 받아서 처리함

'''
import json
import threading
import paho.mqtt.client as mqtt
import time

BROKER_ADDR = '155.230.120.235'
TOKEN_SENSOR = 'sensors/'
TOKEN_THRESHOLD = 'edge/threshold/'
TOKEN_URG = 'urgent/'

MQTT_PORT = 1883
moving_avg_list = list()  # Moving Average를 값을 저장하는 리스트
'''
    MQTT를 이용하여 publish할 data 클래스
    - 센서의 측정 데이터를 JSON 형태로 변환하여 MQTT를 이용하여 전송함 
    JSON dumps() 기능 추가 
'''


class SensorData:
    def __init__(self):
        print('Class of sensor data')
        self.maverage_values = list()  # Moving Average List

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

    def parse_json(self):
        print("Parsing JSON")

# ------------------------------------------------------------------------
'''
    Threshold, Standard deviation, moving average 등을 저장하는 클래스
    JSON Parser 기능 추가   
'''


# ------------------------------------------------------------------------
class ThresholdParameters:
    def __init__(self):
        print("Class of Threshold Parameters")


# ------------------------------------------------------------------------
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

    def convert_threshold_json(self, dev, timestamp, tolerance, thresh_hi, thresh_low, avg):
        '''
            Threshold parameter들을 JSON 형태로 변환하여 문자열로 리턴함
        :return: JSON type의 string
        '''

        threshold_data = dict()
        threshold_data['dev'] = dev
        threshold_data['timestamp'] = timestamp
        threshold_data['tolerance'] = tolerance
        threshold_data['thresh_hi'] = thresh_hi
        threshold_data['thresh_low'] = thresh_low
        threshold_data['avg'] = avg

        threshold_string = json.dumps(threshold_data)
        #print(threshold_string)
        return threshold_string

    def run_publish(self, token, interval):
        '''
           Edge -> IoT Node로 threshold parameter들을 전송함
        :param token:
        :return:
        '''
        print("run_publish")
        # keepalive = 60
        self.connect(BROKER_ADDR, MQTT_PORT, 60)
        self.loop_start()
        count = 1
        while True:
            # devid, timestamp, tolerance, thresh_hi, thresh_low, avg
            threshold_string = self.convert_threshold_json(1, count, 5.0, 0, 100, 2)
            self.publish(token, threshold_string, 1)
            time.sleep(interval)
            count += 1
            if (count > 10):
                break

        print("Publishing Stop")
        self.disconnect()

    def thread_publish(self, token, interval):
        t = threading.Thread(target=self.run_publish, args=(token, interval,))
        #t.daemon = True
        t.start()

    def run_subscribe(self, token, interval):
        print("run_subscribe")
        self.connect(BROKER_ADDR, MQTT_PORT, 60)
        self.subscribe(token, qos=1)
        self.loop_forever(interval)

    def thread_subscribe(self, token, interval):
        t = threading.Thread(target=self.run_subscribe, args=(token, interval, ))
        #t.daemon = True
        t.start()

# ------------------------------------------------------------------------
def mqtt_edge_main():
    '''
        pub_client: Publisher: Sensor node -> Edge node (전송 데이터: 센서 측정값)
        sub_client: Subscriber: Edge node -> Sensor node (전송 데이터: threshold 값)
    :return:
    '''

    print("[ MQTT Edge Main ]")

    sub_client = MQTTClient()  # Subscriber
    #sub_client.run_subscribe(TOKEN_SENSOR, 1)
    sub_client.thread_subscribe(TOKEN_SENSOR, 1)

    pub_client = MQTTClient()  # Publisher
    pub_client.thread_publish(TOKEN_THRESHOLD, 1)

mqtt_edge_main()
