from celery import Celery


# Configure Celery to use RabbitMQ as the message broker and Redis as the result backend
app = Celery('tasks',
             broker='student://localhost:6379/0',
             backend='redis://localhost:6379/0')  # Specify Redis as result backend

@app.task
def power(n, power):
    return n ** power
