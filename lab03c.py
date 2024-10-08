import multiprocessing
import time
def calculate_process_sum(m:int,n:int,q:multiprocessing.Queue):
    sum  = 0
    for i in range(m+1,n+1):
        sum+=i
    q.put(sum)

def calculate_serial_sum(n:int):
    sum  = 0
    for i in range(n+1):
        sum+=i
    return sum

serial_start_time= time.time()
n= 100000000   
serial_sum=calculate_serial_sum(n)
serial_total_time= time.time()-serial_start_time

num_process= 4
n=100000000
num_thread=4
mult=n//num_thread

processes=[]
q = multiprocessing.Queue()

for i in range(num_process):
    x=mult*i
    y= mult*(i+1)
    process = multiprocessing.Process(target=calculate_process_sum,args=(x,y,q))
    processes.append(process)

process_start = time.time()

for process in processes:
    process.start()

for process in processes:
    process.join()

process_sum =0

for i in range(num_process):
    process_sum+=q.get()
process_total_time= time.time()-process_start

print("the sum of first ",n,"is",process_sum)
print("the total time taken is ",process_total_time,"seconds")


process_speedup = serial_total_time/process_total_time
print("the  speedup ",process_speedup)

efficiency = process_speedup / num_process
print("the  efficiency ",efficiency)


P= process_start/(process_total_time+serial_total_time)


speedup_amdahl =  1/(1-P)+(P/4)
print("Amdahl's speedup:", 1/(1-P)+(P/4))
efficiency_amdahl = speedup_amdahl / num_process
print("Amdahl's efficiency :  ",efficiency_amdahl)
speedup_gustafson = (1-P)*(1-4)+4
print("Gustafson's speedup", speedup_gustafson )
efficiency_gustafson = speedup_gustafson / num_process
print("Gustafson's Law Efficiency:", efficiency_gustafson)