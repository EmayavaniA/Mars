from flask import Flask, request
import subprocess
import multiprocessing
import queue
import threading
import sys
import json
app = Flask(__name__)
#script_queue = multiprocessing.Queue()
script_queue = queue.Queue()

def run_subprocess(script_comm):
        print("Inside subprocess ")
        p=subprocess.Popen(script_comm,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        print(p)
        stdout,stderr = p.communicate()
        wait_time = p.wait()
        print("Wait time is ",wait_time)
        if p.returncode == 0:
            print("output is=".format(stdout) )
        else:
            print("output error is =".format( stderr))

def queue_worker():
    while True:
        #print("inside queue_worker")
        script_cmd = script_queue.get()
        #print(script_cmd)
        #process_q = multiprocessing.Process(target=run_subprocess,args=(script_cmd,))
        #subprocess.Popen(script_cmd,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        subprocess.Popen(script_cmd,shell=True)
        script_queue.task_done()

@app.route('/pyprocess', methods=['POST'])
def process_request():
    json_data =request.get_json()
    useCaseType = json_data['UseCaseType']  
    json_dict = json.dumps(json_data)
    if json_data != None:
        x= useCaseType
        y= "  c:/path/Threading"
        scriptrun = sys.executable
        #print(scriptrun)                                                                                                                                                                                                                      
        Parsejson1=str(json_dict).replace(' ','')
        Parsejson2=Parsejson1.replace('"','\\"')
        script_cmd=scriptrun + y+'/'+x +" " + Parsejson2
        #print(script_cmd)
        print(type(script_cmd))
        script_queue.put(script_cmd)
        print(script_queue)
        m= "request added to queue for " +useCaseType
    return m


if __name__ == '__main__':
    #processpy = multiprocessing.Process(target=queue_worker)
    #processpy.start()
    worker_thread = threading.Thread(target=queue_worker)
    worker_thread.start()
    app.run(host='0.0.0.0',debug=True,port =2000)
