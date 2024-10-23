from RPi import GPIO
from threading import Thread
from time import sleep
from display_lcd import lcd, lcd_display_loop
import log_and_send 
import measure_speed 

try:
	measure_speed.init()
	log_and_send.init()
	consecutive = True
	if consecutive:
		lcd.text("Last Speed(o/s):", 1)
	else:
		lcd.text("Last Speed(cm/s):", 1)

	# Separate threads for each function, to run them concurrently
	Thread(target=measure_speed.speed_measure_loop, args=[False, consecutive]).start()
	Thread(target=lcd_display_loop).start()
	Thread(target=log_and_send.log_mqtt_loop).start()

	input("Press Enter to exit...")
except Exception as e:
	print(e)
finally:
	print('Cleaning Up!')
	measure_speed.stop = True

	# Wait for the threads to finish
	sleep(1)

	GPIO.cleanup()
	lcd.clear()
