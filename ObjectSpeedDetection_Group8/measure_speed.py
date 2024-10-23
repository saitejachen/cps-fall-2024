from RPi import GPIO
from time import monotonic, sleep, time

from threading import Thread

# Set up the GPIO pins
FIRST = 5
SECOND = 6
DISTANCE = 0.1
GPIO.setmode(GPIO.BCM)
GPIO.setup(FIRST, GPIO.IN)
GPIO.setup(SECOND, GPIO.IN)

# Set up the variables
def init():
    global last_speed, stop
    last_speed = 0
    stop = False
	
def speed_measure_loop(keep_last = True, consecutive = False):
	global last_speed, stop
	from log_and_send import send_queue

	previous_first = False
	previous_second = False
	first_s = 0
	second_s = 0
	last_print_time = monotonic()
	execution_times = []

	while not stop:
		start_time = monotonic()
		first = not GPIO.input(FIRST)
		second = not GPIO.input(SECOND)

		if first and not previous_first:
			first_s = monotonic()
			print('First:', first_s)
			if second_s or consecutive:
				if consecutive:
					last_speed = round(1 / (first_s - second_s), 2)
					print(f'Speed: {last_speed} o/s')
					send_queue.append((time(),last_speed, -1))
				else:
					last_speed = round(DISTANCE / (first_s - second_s) * 100, 2)
					print(f'Speed: {last_speed} cm/s')
					send_queue.append((time(),last_speed, 1))
				if consecutive:
					second_s = first_s
				else:
					second_s = 0
				if not keep_last and not consecutive:
					first_s = 0

		if not consecutive and second and not previous_second:
			second_s = monotonic()
			print('Second:', second_s)
			if first_s:
				last_speed = round(DISTANCE / (second_s - first_s) * 100, 2)
				print(f'Speed: {last_speed} cm/s')
				send_queue.append((time(),last_speed, 0))
				first_s = 0
				if not keep_last:
					second_s = 0

		previous_first = first
		previous_second = second
		
		# Measure the execution time
		end_time = monotonic()
		execution_time = end_time - start_time
		execution_times.append(execution_time)

		# Print the execution time every 60 seconds
		if end_time - last_print_time >= 60:
			min_time = min(execution_times)
			max_time = max(execution_times)
			avg_time = sum(execution_times) / len(execution_times)
			print(f'Execution Time (min,avg,max) us: {round(min_time * 10**6, 2)}, {round(avg_time * 10**6, 2)}, {round(max_time * 10**6, 2)}')
			last_print_time = end_time
			execution_times = []

		sleep(max(0,0.001 - (monotonic() - start_time)))