import random
import threading
import time
from queue import Queue

# Global dictionaries to store temperatures
latest_temperatures = {}
temperature_averages = {}

# Lock for synchronization
lock = threading.RLock()

# Queue for storing temperatures
temperature_queue = Queue()

# Sensor simulation function
def simulate_sensor(sensor_id):
    while True:
        with lock:
            temperature = random.randint(15, 40)
            latest_temperatures[sensor_id] = temperature
            temperature_queue.put((sensor_id, temperature))
        time.sleep(1)  # Update every 1 second

# Process temperatures and calculate averages
def process_temperatures():
    sensor_data = {}
    
    while True:
        with lock:
            while not temperature_queue.empty():
                sensor_id, temp = temperature_queue.get()
                if sensor_id not in sensor_data:
                    sensor_data[sensor_id] = []
                sensor_data[sensor_id].append(temp)
                # Keep only the last 10 temperatures
                if len(sensor_data[sensor_id]) > 10:
                    sensor_data[sensor_id].pop(0)
                
                # Calculate average for each sensor
                temperature_averages[sensor_id] = sum(sensor_data[sensor_id]) / len(sensor_data[sensor_id])
        time.sleep(5)  # Update every 5 seconds

# Initialize display layout
def initialize_display():
    print("Current temperatures:")
    print(f"Latest Temperatures: Sensor 1: --°C Sensor 2: --°C Sensor 3: --°C")
    print(f"Sensor 1 Average:                                                    --°C")
    print(f"Sensor 2 Average:                                                    --°C")
    print(f"Sensor 3 Average:                                                    --°C")

# Update display in real-time
def update_display():
    while True:
        with lock:
            print("\033[H\033[J", end="")  # Clear the console (simulating screen update)
            print("Current temperatures:")
            for sensor_id in range(3):
                print(f"Sensor {sensor_id}: {latest_temperatures.get(sensor_id, '--')}°C ", end="")
            print()
            for sensor_id in range(3):
                print(f"Sensor {sensor_id} Average: {temperature_averages.get(sensor_id, '--'):>2.2f}°C")
        time.sleep(5)  # Update every 5 seconds

# Main function
def main():
    # Initialize display
    initialize_display()
    
    # Create and start sensor threads
    for sensor_id in range(3):
        threading.Thread(target=simulate_sensor, args=(sensor_id,), daemon=True).start()

    # Start data processing thread
    threading.Thread(target=process_temperatures, daemon=True).start()

    # Start display update thread
    threading.Thread(target=update_display, daemon=True).start()

    # Keep main thread running to allow daemon threads to run
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
