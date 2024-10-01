import time 
import threading
result = []
def calculate_serial_sum(n:int):
    sum  = 0
    for i in range(n+1):
        sum+=i
    return sum
def calculate_sum(m: int, n: int):
    sum=0
    for i in range(int(m+1),int(n+1)):
        sum+=i
    result.append(sum)
    return sum
serial_start_time= time.time()
n= 100000000
serial_sum=calculate_serial_sum(n)
serial_total_time= time.time()-serial_start_time
print(f"Sum of first {n} is: {serial_sum}")
print("Time Taken:", serial_total_time,"seconds")



num_thread=16
threads=[]
x=0
mult=n/num_thread
threat_st = time.time()
for i in range(0,num_thread):
    x=mult*i
    y= mult*(i+1)
    thread = threading.Thread(target=calculate_sum, args=(x,y))
    threads.append(thread)
    thread.start()


for thread in threads:
    thread.join()

    
thread_total_time= time.time()-threat_st
thread_sum = sum(result)


print("Parallel Results")
print(f"Sum of first {n} is: {thread_sum}")
print("Time Taken:", thread_total_time,"seconds")


thread_speedup = (serial_total_time)/(thread_total_time)
print(f"Speedup: {thread_speedup}")

efficiency = thread_speedup / num_thread
print(f"Efficiency: {efficiency}")
