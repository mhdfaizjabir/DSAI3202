from tasks import power

def dispatch_tasks():
    # Dispatch tasks asynchronously
    result_objs = [power.apply_async((number, 2)) for number in range(1, 10001)]
    
    # Collect results
    results = [result.get() for result in result_objs]
    return results

if __name__ == "__main__":
    results = dispatch_tasks()
    print(results[:10])  # Print the first 10 results
