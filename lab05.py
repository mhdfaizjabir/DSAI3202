import time
import random
from multiprocessing import Pool
import concurrent.futures

# Function to compute the square of a number
def square(n):
    return n * n

# Create a list of 10^7 random integers
numbers = []
for _ in range(10**7):
    numbers.append(random.randint(1, 1000))


# Scenario 1: Sequential for loop
start = time.time()
squares_seq = []
for num in numbers:
    squares_seq.append(square(num))
print(f"Sequential for loop time: {time.time() - start:.4f} seconds")


# Scenario 2: Multiprocessing with apply()
def worker_apply(num):
    return square(num)

if __name__ == "__main__":
    start = time.time()
    squares_apply = []
    with Pool() as pool:
        for num in numbers:
            squares_apply.append(pool.apply(worker_apply, args=(num,)))
    print(f"Multiprocessing pool apply() time: {time.time() - start:.4f} seconds")


# Scenario 3: Multiprocessing with map()
if __name__ == "__main__":
    start = time.time()
    with Pool() as pool:
        squares_map = pool.map(square, numbers)
    print(f"Multiprocessing pool map() time: {time.time() - start:.4f} seconds")


# Scenario 4: Concurrent futures ProcessPoolExecutor
if __name__ == "__main__":
    start = time.time()
    squares_futures = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for result in executor.map(square, numbers):
            squares_futures.append(result)
    print(f"ProcessPoolExecutor time: {time.time() - start:.4f} seconds")
