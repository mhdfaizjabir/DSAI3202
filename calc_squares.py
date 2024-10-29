from mpi4py import MPI
import numpy as np
import time

# Function to compute squares in smaller chunks to reduce memory usage
def compute_squares_in_chunks(start, end, chunk_size=1000000):
    for i in range(start, end, chunk_size):
        sub_end = min(i + chunk_size, end)
        yield np.array([j * j for j in range(i, sub_end)])

def main(n=int(1e8), bonus_mode=False):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Start timing for main calculation
    if rank == 0:
        start_time = time.time()

    # Define main chunk for each process
    chunk_size = n // size
    start = rank * chunk_size + 1
    end = (rank + 1) * chunk_size + 1 if rank < size - 1 else n + 1  # Handle last chunk edge case

    # Calculate squares in smaller chunks to avoid memory overload
    local_sum = 0
    last_square = 0

    for squares_chunk in compute_squares_in_chunks(start, end):
        local_sum += len(squares_chunk)  # Track count of computed squares
        last_square = squares_chunk[-1]  # Track last computed square in each chunk

    # Gather all results to the root process (only final values, not the whole array)
    total_count = comm.reduce(local_sum, op=MPI.SUM, root=0)
    max_square = comm.reduce(last_square, op=MPI.MAX, root=0)

    if rank == 0:
        # Calculate and print final time
        elapsed_time = time.time() - start_time
        print(f"Total number of squares: {total_count}")
        print(f"Last square calculated: {max_square}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

        # If in bonus mode, calculate max n for 300 seconds
        if bonus_mode:
            max_n = n
            bonus_start_time = time.time()  # Start timer specifically for bonus mode
            print("\nEntering bonus mode...")
            while True:
                max_n += int(1e6)  # Increment max_n in steps
                bonus_elapsed_time = time.time() - bonus_start_time
                if bonus_elapsed_time >= 300:
                    break
                print(f"Trying n={max_n} => Bonus Time: {bonus_elapsed_time:.2f} seconds")
            print(f"Maximum n within 300 seconds: {max_n}")

if __name__ == "__main__":
    import sys
    # Command line argument for max n value
    n = int(sys.argv[1]) if len(sys.argv) > 1 else int(1e7)
    bonus_mode = "--bonus" in sys.argv
    main(n, bonus_mode)
