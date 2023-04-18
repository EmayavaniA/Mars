import sys
import json
from simple_salesforce import Salesforce
import subprocess
from subprocess import Popen, PIPE
from flask import Flask, jsonify, request,abort,redirect,url_for
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, Api
from pyfunctions import *
import queue
import threading

auth = HTTPBasicAuth()
@auth.verify_password
def verify(username, password):
    u_name = "aaa"
    p_word = "ppp"
    if (not(username) or not(password)) or (username==None or password == None):
        return False
    elif username in u_name and password in p_word:
        return True
    else:
        return False


app = Flask(__name__)
script_queue = queue.Queue()

@app.route('/loginpy', methods=['GET','POST'])
@auth.login_required
def private_page():
      return redirect(url_for('pyApiController'),code=307)


def queue_worker():
    while True:
        script_cmd = script_queue.get()
        subprocess.Popen(script_cmd,shell=True)
        script_queue.task_done()


@app.route('/cccController', methods=['POST'])
def cccController():
    try:
        json_data =request.get_json()
        useCaseType = json_data['UseCaseType']
        json_dict = json.dumps(json_data)
        print(type(json_dict))
        if json_dict != None:
            #x,y = scriptlookup(useCaseType)
            x= "filename.py "
            y= "  /home/user/project"
            scriptrun = sys.executable
            logging.info(scriptrun)
            Parsejson1=str(json_dict).replace(' ','')
            Parsejson2=Parsejson1.replace('"','\\"')
            Parsejson3=json.dumps(Parsejson2)
            script_cmd=scriptrun + y+'/'+x +Parsejson2
            #logging.info("script_cmd= ",script_cmd)
            logging.info(script_cmd)
            logging.info(type(script_cmd))
            script_queue.put(script_cmd)
            m= " Request added to queue for " +useCaseType
        return m
    except Exception as e:
        logging.info(e)
        #sys.exit(1)

if __name__ == '__main__':
    connection = None
    logger = getLogger("filename")
    try:
        worker_thread = threading.Thread(target=queue_worker)
        worker_thread.start()
        app.run(host='0.0.0.0',debug=True,port =80)
    except Exception as e:
        logging.info("Error in main: %s", repr(e))
    finally:
         if connection is not None and connection.is_connected():
            connection.close()
