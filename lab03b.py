import threading 
import time 

def calculate_sum_for_threads(start :int = 0,end: int =10,results_list=[] ):
    thread_Sum=0
    for i in range ( start , end ):
        thread_Sum += i

    results_list.append(thread_Sum)

n=int(1e8)

number_threads = 3

step = n//number_threads

threads = []

results = []


for i in range (number_threads):
    start_thread = i * step + 1
    end_thread = (i+1)*step
    thread = threading.Thread(target=calculate_sum_for_threads,
                           args=(start_thread, 
                             end_thread,
                              results))
    
    threads.append(thread)

start_time  = time.time()

for i in range(number_threads):
    threads[i].start()

for i in range(number_threads):
    threads[i].join()


end_time = time.time()

print ( end_time-start_time)