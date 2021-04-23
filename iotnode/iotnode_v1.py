import os
import sys
import serial
import time
import datetime
from threading import Thread
import csv

#-----------------------------------------
# Definitions
#-----------------------------------------
PORT_NUM = '/dev/ttyS0'
#BAUD = 115200
BAUD = 9600

#-----------------------------------------
# Global Variables
#-----------------------------------------
rx_values = [0.0 for i in range(4)]
file_save = 'off'
CSV_PATH = 'data/'
flag_fopen = False
repeat_time = 0
interval = 5	# timer interval

'''
def save_data(fname, date_time_str, values):
    global file_save
    global flag_fopen
	global repeat_time

    filename = CSV_PATH + date_time_str + '_sensor.csv'
    csv_data_file = open(fname, 'a', encoding='utf-8')
    csv_writer = csv.writer(csv_data_file, delimiter=',')

    csv_writer.writerow([date_time_str, values[0], values[1], values[2], values[3]])
    csv_data_file.close()
'''

def rx_data_count_save(name, port, endtime):
    '''
        라즈베리파이의 시리얼 포트를 이용하여 Arduino에서 전송되는 센서 데이터를 읽어 들임
        file_save == on: 시간정보_sensor.csv 파일에 센서 데이터를 저장함

        Rx sensor data from Arduino
        +--------+-------+-------------+----------+
        | PM 2.5 | PM 10 | Temperature | Humidity |
        +--------+-------+-------------+----------+
           int      int       float        float


    :param name:
    :param port:
    :param repeat:
    :return:
    '''
    global file_save
    global repeat_time
    global interval

    repeat_time = endtime
    print('Rx_data Thread: {0}, Time: {1}'.format(name, repeat_time))

    now = datetime.datetime.now()
    start_time_str = now.strftime("%Y-%m-%d-%H%M%S")
    start_time = now

    filename = CSV_PATH + start_time_str + '_sensor.csv'
    csv_data_file = open(filename, 'a', encoding='utf-8')
    csv_writer = csv.writer(csv_data_file, delimiter=',')

    curr_time = datetime.datetime.now()
    time_diff = curr_time - start_time
    count = 0

    # 0 <= timediff.seconds < 86399 (24시간: 86400초 측정시 문제가 발생했었음)
    while (time_diff.total_seconds() < repeat_time):
        # 시리얼 포트를 통해 들어온 데이터를 한 라인씩 읽어들임
        rx_bytes = port.readline()

        # remove \r\n and convert bytes to string
        # split string with the delimiter(',')
        #if(rx_bytes[-2] != '\r' and rx_bytes[-1] != '\n'):
        #    continue

        values = rx_bytes[:-2].decode().split(',')
        if(len(values) < 4 or len(values) > 4):
            continue

        try:
            for i in range(len(rx_values)):
                if(values[i] != ''):
                    if(i == 0 or i == 1):
                        rx_values[i] = int(values[i])
                	else:
                        rx_values[i] = float(values[i])
                else:
                    rx_values[i] = 0.0
        except (IndexError, ValueError):
            print("IndexError or ValueError: {0}: {1}, len={2}".format(i, count, len(values)))
        except :
            print("Exception: {0}: {1}".format(count, values))

        current_time = datetime.datetime.now()
        date_time_str = current_time.strftime("%Y-%m-%d,%H.%M.%S")

        count += 1
        #repeat_time -= 1
        print("{0:6d}: {1}, {2}".format(count, date_time_str, rx_values), end=" ")
        csv_writer.writerow([date_time_str, rx_values[0], rx_values[1], rx_values[2], rx_values[3]])
        time.sleep(interval) # interval(5초) 간격마다 데이터 수집

        current_time = datetime.datetime.now()
        time_diff = current_time - start_time
        print("diff: {0}/ {1}".format(time_diff.seconds, repeat_time))

    csv_data_file.close()
    port.close()
    print("Sensor data is written in {0}. Count: {1}".format(filename, count))

    current_time = datetime.datetime.now()
    end_time_str = current_time.strftime("%Y-%m-%d,%H.%M.%S")
    print("Start:{0}, Diff: {1}, End:{2}".format(start_time_str, time_diff.total_seconds(), end_time_str))


def rx_data_count(name, port, repeat_time):
    '''
        라즈베리파이의 시리얼 포트를 이용하여 Arduino에서 전송되는 센서 데이터를 읽어 들임
        file_save == on: 시간정보_sensor.csv 파일에 센서 데이터를 저장함

        Rx sensor data from Arduino
        +--------+-------+-------------+----------+
        | PM 2.5 | PM 10 | Temperature | Humidity |
        +--------+-------+-------------+----------+
           int      int       float        float


    :param name:
    :param port:
    :param repeat:
    :return:
    '''
    global file_save
    global interval
    filename = ''

    print('Rx_data Thread: {0}, Time: {1}'.format(name, repeat_time))

    now = datetime.datetime.now()
    date_time_str = now.strftime("%Y%m%d%H%M%S")
    start_time = now
    curr_time = datetime.datetime.now()

    time_diff = curr_time - now
    count = 0
    while (time_diff.total_seconds() <= repeat_time):
        # 시리얼 포트를 통해 들어온 데이터를 한 라인씩 읽어들임
        rx_bytes = port.readline()

        # remove \r\n and convert bytes to string
        # split string with the delimiter(',')
        #if(rx_bytes[-2] != '\r' and rx_bytes[-1] != '\n'):
        #    continue

        values = rx_bytes[:-2].decode().split(',')
        if(len(values) < 4 or len(values) > 4):
            continue

        try:
            for i in range(len(rx_values)):
                if(values[i] != ''):
                    rx_values[i] = float(values[i])
                else:
                    rx_values[i] = 0.0
        except (IndexError, ValueError):
            print("IndexError or ValueError: {0}: {1}, len={2}".format(i, count, len(values)))
        except :
            print("Exception: {0}: {1}".format(count, values))

        current_time = datetime.datetime.now()
        date_time_str = current_time.strftime("%Y.%m.%d.%H.%M.%S")
        count += 1
        #repeat_time -= 1
        print("{0:6d}: {1}, {2}".format(count, date_time_str, rx_values))
        #----------------------------------------------------------------
        #    Socket 통신 기능 추가
        #----------------------------------------------------------------



        time.sleep(interval)
        current_time = datetime.datetime.now()
        time_diff = current_time - start_time

    port.close()
    print("Simulation finished and serial port closed.")

def make_init_dir(dirname):
    '''
        기존에 dirname의 폴더가 없는 경우 폴더를 생성함

        :param dirname:
        :return:
    '''
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    else:
        print("{0} already exists.".format(dirname))

def iotnode_main():
    global file_save
    sim_count = 0

    # Serial Port Open
    port = serial.Serial(PORT_NUM, BAUD)

    if(len(sys.argv) <= 2):
        print("Usage: iotnode.py timeout [on|off] ")
        sim_count = 10
        file_save = 'off'
    else:
        sim_count = int(sys.argv[1])
        print('Timeout: ', sim_count)
        file_save = sys.argv[2]

    make_init_dir(CSV_PATH)
    if(file_save == 'off'):
        trx = Thread(target=rx_data_count, args=('Rx Thread', port, sim_count))
        trx.start()
    else:
        trx_save = Thread(target=rx_data_count_save, args=('Rx Thread File Save', port, sim_count))
        trx_save.start()

iotnode_main()
