import time
import random
from datetime import datetime
import paho.mqtt.client as mqtt
import measure_speed

# MQTT broker details
broker = 'broker.emqx.io'
port = 1883
topic = 'group_8/project'

# Create an MQTT client
client = mqtt.Client()

# Connect to the broker
client.connect(broker, port, 60)

# For logging
yyyy_mm_dd = datetime.now().strftime('%Y-%m-%d')
log_file_name =f'log_{yyyy_mm_dd}.csv'

def init():
    global send_queue
    send_queue = []

def log_mqtt_loop():
    global send_queue, log_file_name
    
    last_print_time = time.monotonic()
    execution_times = []

    while not measure_speed.stop:
        start_time = time.monotonic()
        
        with open(log_file_name, 'a') as log_file:
            while send_queue:
                timestamp, speed, direction = send_queue.pop(0)
                pretty_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                info = client.publish(topic, f'{pretty_time},{speed},{direction}')
                log_file.write(f'{pretty_time},{speed},{direction}\n')
                status = info.rc
                if status != 0:
                    print(f'Error: {info}')
                    if status == mqtt.MQTT_ERR_CONN_LOST or status == mqtt.MQTT_ERR_NO_CONN:
                        client.reconnect()
                        print('Reconnected to the broker')
                        send_queue.insert(0, (timestamp, speed, direction))
   
                print(f'Sent: {pretty_time},{speed},{direction} \t Status: {info.rc}')
        
        end_time = time.monotonic()
        execution_time = end_time - start_time
        execution_times.append(execution_time)

        if end_time - last_print_time >= 60:
            min_time = min(execution_times)
            max_time = max(execution_times)
            avg_time = sum(execution_times) / len(execution_times)
            print(f'Log MQTT Execution Time (min,avg,max) ms: {round(min_time * 10**3, 2)}, {round(avg_time * 10**3, 2)}, {round(max_time * 10**3, 2)}')
            last_print_time = end_time
            execution_times = []

        time.sleep(max(0, 5 - (time.monotonic() - start_time)))


if __name__ == '__main__':
    while True:
        speed = random.randint(0, 100)
        direction = random.randint(0, 1)
        send_queue.append((speed, direction))
        time.sleep(1)

