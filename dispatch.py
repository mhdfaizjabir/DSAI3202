from tasks import power
import time

# def dispatch_tasks():
#     result_objs = [power.apply_async((number, 2))
#                    for number in range(1, 1000001)]
#     results = [result.get()
#                for result in result_objs]
#     return results

# if __name__ == "__main__":
#     start= time.time()
#     results = dispatch_tasks()
#     print(results[:10])
#     print(f"Time Taken: {time.time()-start}")



def dispatch_batches(data, batch_size=100):
    # Split the data into batches
    batches = [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

    # Dispatch each batch to Celery workers
    result_objs = [power.apply_async((batch,)) for batch in batches]

    # Wait for all results (batches) to finish and collect them
    results = [result.get() for result in result_objs]
    print(f"Calculating tasks done, Time Taken:{time.time()-start} seconds")
    print("Now aggregating the results")

    combined_results = [item for batch in results for item in batch]

    return combined_results

start = time.time()
data = list(range(10000001))
results = dispatch_batches(data, batch_size=1000)  # Process in batches of 100
print(results[:10])  # Print first 10 batch results
print(f"Time taken {time.time()-start} seconds")
print(f"Length of result {len(results)}")