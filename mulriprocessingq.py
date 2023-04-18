from flask import Flask, request
import subprocess
import queue
import threading

app = Flask(__name__)

# create a queue to hold incoming requests
request_queue = queue.Queue()

def worker():
    while True:
        # get the next request from the queue
        request_data = request_queue.get()
        # create a subprocess to run the appropriate script
        subprocess.run(["python", f"{request_data['script_name']}.py", str(request_data['request_data'])])
        # mark the request as complete in the queue
        request_queue.task_done()

# create a thread to run the worker function
worker_thread = threading.Thread(target=worker)
worker_thread.start()

@app.route('/api', methods=['POST'])
def handle_request():
    # get the script name and request data from the POST request
    script_name = request.form['script_name']
    request_data = request.form['request_data']
    # add the request to the queue
    request_queue.put({'script_name': script_name, 'request_data': request_data})
    # return a response to the client immediately
    return 'Request received'

if __name__ == '__main__':
    app.run(debug=True)
