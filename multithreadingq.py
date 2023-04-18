import multiprocessing

def process_request(request):
# Process the request here
    print(f"Processing request {request}")

if __name__ == "__main__":
# Define the requests to process
    requests = [1, 2, 3, 4, 5]

# Create a pool of worker processes
pool = multiprocessing.Pool()

# Process the requests in parallel
pool.map(process_request, requests)

# Close the pool and wait for all processes to finish
pool.close()
pool.join()
