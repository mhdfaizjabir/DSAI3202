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

n = int(1e8*4)

chunk_size = n // size
if rank == size - 1:  # Last rank takes any remaining values
    end = n + 1
else:
    end = (rank + 1) * chunk_size + 1
start = rank * chunk_size + 1

# Time the calculation of squares
start_square_time = time.time()
print(f"Rank {rank} processing range: {start} to {end-1}")

square_list = squares(start, end)

end_square_time = time.time()

# Print start and end ranges
print(f"Rank {rank} processing range: {start} to {end-1}")

# Print time taken for each process
print(f"Time taken for {rank} is {(end_square_time - start_square_time):.4f} seconds")

# Gather results
total_squares = comm.gather(square_list, root=0)

if rank == 0:
    # Flatten the list of lists
    total_squares = [item for sublist in total_squares for item in sublist]
    print(f"Total Time Taken: {(time.time() - total_time):.4f} seconds")
    print(total_squares[-1])  # Print the last square calculated
    print(len(total_squares))
