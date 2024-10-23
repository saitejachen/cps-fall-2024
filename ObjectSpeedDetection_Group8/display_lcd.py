from rpi_lcd import LCD
from time import monotonic, sleep
import measure_speed

# Set up the LCD
lcd = LCD()

def lcd_display_loop():
	last_print_time = monotonic()
	execution_times = []
	
	while not measure_speed.stop:
		start_time = monotonic()
		lcd.text(str(measure_speed.last_speed), 2)

		end_time = monotonic()
		execution_time = end_time - start_time
		execution_times.append(execution_time)

		if end_time - last_print_time >= 60:
			min_time = min(execution_times)
			max_time = max(execution_times)
			avg_time = sum(execution_times) / len(execution_times)
			print(f'LCD Execution Time (min,avg,max) ms: {round(min_time * 10**3, 2)}, {round(avg_time * 10**3, 2)}, {round(max_time * 10**3, 2)}')
			last_print_time = end_time
			execution_times = []
		
		sleep(max(0,0.2 - (monotonic() - start_time)))