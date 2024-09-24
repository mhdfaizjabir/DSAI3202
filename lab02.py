import threading
import multiprocessing
import time
import random
import string

def join_random_letters():
	letter = [random.choice(string.ascii_letters) for  _ in range(int(1000))]
	word  = ''.join(letter)
	return word

def add_random_numbers():
	numbers = [random.randint(0,100) for _ in range(int(1000))]
	total_sum = sum(numbers)
	return total_sum



serial_start_time =time.time()
join_random_letters()
add_random_numbers()
serial_end_time =time.time()


parallel_start_time =time.time()
word_thread =threading.Thread(target = join_random_letters)
sum_thread = threading.Thread(target = add_random_numbers)

word_thread.start()
sum_thread.start()
word_thread.join()
sum_thread.join()
parallel_end_time =time.time()


process_start_time =time.time()
word_process =multiprocessing.Process(target = join_random_letters)
sum_process = multiprocessing.Process(target = add_random_numbers)

word_process.start()
sum_process.start()
word_process.join()
sum_thread.join()
process_end_time =time.time()

thread_speedup = (serial_end_time-serial_start_time)/(parallel_end_time-parallel_start_time)
process_speedup =(serial_end_time-serial_start_time)/(process_end_time-process_start_time)

serial_time = serial_end_time-serial_start_time
parallel_time = parallel_end_time-parallel_start_time
total_time = parallel_end_time-serial_start_time
P= parallel_time/total_time

print("Speedup(Thread): ",thread_speedup)
print("Speedup(Process): ", process_speedup )
print("Efficiency(Thread):",thread_speedup/4)
print("Efficiency(Process):",process_speedup/4)
print("P", P)
print("Amdahl's speedup:", 1/((1-P)+(P/4)))
print("Gustafson's speedup : ", (1-P)*(1-4)+4)