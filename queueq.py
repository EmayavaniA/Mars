import queue

def process_request(request):
# Process the request here
    print(f"Processing request {request}")

if __name__ == "__main__":
# Define the requests to process
    requests = [1, 2, 3, 4, 5]

# Create a queue to hold the requests
request_queue = queue.Queue()

# Add the requests to the queue
for request in requests:
    request_queue.put(request)

# Process the requests in sequence
while not request_queue.empty():
    request = request_queue.get()
    process_request(request)
