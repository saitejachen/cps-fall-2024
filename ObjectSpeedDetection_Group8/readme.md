# Usage
To run the project, on raspberrypi

1) Simple mode: Suitable if you want to capture the speed of the objects passing by. Utilizes two sensors.

    ```
    python3 project_group8.py
    ```

2) Consecutive mode: SUitable if you want to check how frequently objects are appearing.

    To run in consecutive mode
    ```
    python3 project_group8.py true
    ```

# File information:

- [project_group8.py](project_group8.py) is the main threads/loops runner. It handles the start/stop of the program.
- [measure_speed.py](measure_speed.py) handles the sensor. It measures the speed when the sensors are triggered. Also, it calls the log and send function.
- [log_and_send.py](log_and_send.py) is for logging and sending the measured speed via MQTT. 
- [display_lcd.py](display_lcd.py) has a single functionality to update whatever the last speed was recorded.

# log file

Whenever you run the program, a log file with today's date would be generated. All the speeds recoreded are saved with a time stamp.

For example,
`log_2024-10-23.csv`
```csv
2024-10-23 15:16:40.894187,6.26,1
2024-10-23 15:16:42.027405,8.83,1
2024-10-23 15:16:42.920202,11.19,1
```
- Column 0: Time
- Column 1: Recorded speed
- Column 2: Direct of the object

# View client

The client utilizes the data sent over the MQTT to make a line and a frequency distribution to visualize the speed of the object.

There are two available view clients:
1) [Simple view client](view_client.html) : To display the speed and the direction of objects that are passing by. (cm/s)

2) [Consecutive view client](view_client_object.html): To display the speed of the objects passing by. (objects/second)