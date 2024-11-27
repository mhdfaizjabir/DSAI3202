from mpi4py import MPI
import numpy as np
import time

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Grid dimensions
GRID_HEIGHT = 10
GRID_WIDTH = 10
STEPS = 10
SLEEP_TIME = 0.2  

# Calculate local grid dimensions
local_height = GRID_HEIGHT // size
if rank < GRID_HEIGHT % size:
    local_height += 1

def initialize_local_grid(local_height, width):
    """Initialize local grid randomly"""
    return np.random.choice([0, 1], size=(local_height, width), p=[0.85, 0.15])

def count_neighbors(grid, i, j):
    """Count live neighbors for cell at position (i, j)"""
    rows, cols = grid.shape
    count = 0
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            if di == 0 and dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                count += grid[ni, nj]
    return count

def update_grid(grid, top_row=None, bottom_row=None):
    """Update grid according to Game of Life rules"""
    rows, cols = grid.shape
    new_grid = np.zeros_like(grid)
    
    # Create extended grid with ghost rows
    extended_grid = np.copy(grid)
    if top_row is not None:
        extended_grid = np.vstack([top_row, extended_grid])
    if bottom_row is not None:
        extended_grid = np.vstack([extended_grid, bottom_row])
    
    # Update cells based on Game of Life rules
    for i in range(rows):
        for j in range(cols):
            # Adjust index for extended grid
            grid_i = i + (1 if top_row is not None else 0)
            neighbors = count_neighbors(extended_grid, grid_i, j)
            
            if extended_grid[grid_i, j] == 1:  # Live cell
                if neighbors < 2 or neighbors > 3:
                    new_grid[i, j] = 0  # Cell dies
                else:
                    new_grid[i, j] = 1  # Cell survives
            else:  # Dead cell
                if neighbors == 3:
                    new_grid[i, j] = 1  # Cell becomes alive
                
    return new_grid

def print_grid(grid):
    """Print the grid using unicode characters"""
    for row in grid:
        print(''.join(['■' if cell else '□' for cell in row]))
    print()

# Initialize local grid
local_grid = initialize_local_grid(local_height, GRID_WIDTH)

# Main simulation loop
for step in range(STEPS):
    # Exchange ghost rows
    top_ghost_row = None
    bottom_ghost_row = None
    
    if rank > 0:  # Send top row to rank-1
        comm.send(local_grid[0], dest=rank-1, tag=0)
    if rank < size-1:  # Send bottom row to rank+1
        comm.send(local_grid[-1], dest=rank+1, tag=1)
    
    if rank > 0:  # Receive bottom ghost row from rank-1
        top_ghost_row = comm.recv(source=rank-1, tag=1)
    if rank < size-1:  # Receive top ghost row from rank+1
        bottom_ghost_row = comm.recv(source=rank+1, tag=0)
    
    # Update local grid
    local_grid = update_grid(local_grid, top_ghost_row, bottom_ghost_row)
    
    # Gather all local grids to root process
    gathered_grids = comm.gather(local_grid, root=0)
    
    # Visualize the complete grid on root process
    if rank == 0:
        full_grid = np.vstack(gathered_grids)
        print(f"\nStep {step + 1}")
        print_grid(full_grid)
        time.sleep(SLEEP_TIME)

MPI.Finalize()