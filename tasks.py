from celery import Celery


# Configure Celery to use RabbitMQ as the message broker and Redis as the result backend
app = Celery('tasks',broker='redis://10.102.0.106:6379/0', backend='redis://10.102.0.106:6379/0')  # Specify Redis as result backend

# @app.task
# def power(n, power):
#     return n ** power

@app.task
def power(numbers):
    # Process a batch of numbers
    return [n ** 2 for n in numbers]

