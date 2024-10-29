import numpy as np
from mpi4py import MPI
import time
from concurrent.futures import ProcessPoolExecutor
from calculate_squares import squares

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
total_time = time.time()

# Total number of elements
n = int(1e8*4.5)

# Calculate chunk size for each MPI rank
chunk_size = n // size
if rank == size - 1:  # Last rank takes any remaining values
    end = n + 1
else:
    end = (rank + 1) * chunk_size + 1
start = rank * chunk_size + 1

# Define helper function for calculating squares in each range
def process_chunk(chunk_range):
    start, end = chunk_range
    return squares(start, end)  # Assume squares function calculates squares of numbers in range

# Function to calculate squares in parallel within each rank
def parallel_squares(start, end, num_processes=4):
    # Define smaller chunks for process-level parallelism
    sub_chunk_size = (end - start) // num_processes
    ranges = [(start + i * sub_chunk_size, start + (i + 1) * sub_chunk_size) for i in range(num_processes)]
    ranges[-1] = (ranges[-1][0], end)  # Ensure last process covers till 'end'

    # Use ProcessPoolExecutor to map each range to the process_chunk function
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        results = list(executor.map(process_chunk, ranges))  # Map each tuple in ranges to process_chunk

    # Flatten list of results
    return [item for sublist in results for item in sublist]

# Time the calculation of squares
start_square_time = time.time()
print(f"Rank {rank} processing range: {start} to {end-1}")

# Calculate squares in parallel
square_list = parallel_squares(start, end)

end_square_time = time.time()

# Print processing range and time taken for each rank
print(f"Rank {rank} processing range: {start} to {end-1}")
print(f"Time taken for rank {rank} is {(end_square_time - start_square_time):.4f} seconds")

# Gather results from all ranks to the root process
total_squares = comm.gather(square_list, root=0)

if rank == 0:
    # Flatten the list of lists from all ranks
    total_squares = [item for sublist in total_squares for item in sublist]
    print(f"Total Time Taken: {(time.time() - total_time):.4f} seconds")
    print(total_squares[-1])  # Print the last square calculated
    print(len(total_squares))
