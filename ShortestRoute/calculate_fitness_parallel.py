from celery import Celery
import numpy as np
from genetic_algorithms_functions import calculate_fitness

app = Celery('genetic_algorithm',
                broker='redis://10.102.0.106:6379/0',
                backend='redis://10.102.0.106:6379/0')


app.conf.update(task_serializer = 'json',
                result_serializer='json',
                accept_content=['pickle', 'json'])
@app.task
def calculate_fitness_chunk_task(chunk, distance_matrix):
    """Calculate fitness for a chunk of routes."""
    distance_matrix = np.array(distance_matrix)
    fitness_values = [
        calculate_fitness(route, distance_matrix) for route in chunk
    ]
    return fitness_values