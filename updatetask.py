from mysql.connector import Error , MySQLConnection
import logging
from configparser import ConfigParser
import json
from simple_salesforce import Salesforce
import subprocess
from subprocess import Popen, PIPE
from flask import Flask, jsonify, request
import requests

#app=Flask(__name__)

#@app.route("/updateticket", methods =["POST"])
def updateticket(sys_id,payloaddata):
    try:
        #payload = json.dumps(payloaddata)
        payload = payloaddata
        ritm_numb = sys_id
        parser = ConfigParser()
        config_file_path = 'c:/pTH/db_config.ini'  # full absolute path here!
        parser.read(config_file_path)
        sn = {}
        if parser.has_section("servicenow"):
            items = parser.items("servicenow")
            for item in items:
                sn[item[0]] = item[1]
        else:
            logging.debug("Error in read ConfigParser")
            print("Error in read ConfigParser")
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.patch(url=sn['url']+ ritm_numb, auth=(sn['user'], sn['pwd']), headers=headers ,data=payload)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
           # Decode the JSON response into a dictionary and use the data
        data = response.json()
        print(data)
    except Exception as e:
        raise Exception(e)
    return data


sysID='DSFEF'

payload_data = json.dumps({
           "work_notes":"Ticket closed by python script Testing",
            "close_notes": "close notes",
            "state": "3",
            "close_code": "Closed/Resolved by Automation",
            "comments": "updating RITM to create task"
            })
#updateticket(sysID,payload_data)

def updatetask(task_id,payloaddata):
    try:
        #payload = json.dumps(payloaddata)
        payloadtsk = payloaddata
        tasknum = task_id
        parser = ConfigParser()
        config_file_path = 'c:/U/db_config.ini'  # full absolute path here!
        parser.read(config_file_path)
        sn = {}
        if parser.has_section("servicenow"):
            items = parser.items("servicenow")
            for item in items:
                sn[item[0]] = item[1]
        else:
            logging.debug("Error in read ConfigParser")
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.patch(url=sn['urlt']+ tasknum, auth=(sn['user'], sn['pwd']), headers=headers ,data=payloadtsk)
        if response.status_code != 200:
            logging.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        data = response.json()
        print(data)
        return "Success"
    except Exception as e:
        raise Exception(e)

task_id='awfdse'
result = ('Permissionsets are already available for the user', 'email@group.com')
payloaddatatask = json.dumps({
            "close_notes": result,
            "state": "3",
            "comments": "task closed",
            "work_notes":"closing the ticket testing"
            })
updatetask(task_id,payloaddatatask)


def updatetask1(task_id,payloaddata):
    try:
        payload = json.dumps(payloaddata)
        #payload = (payloaddata)
        tasknum = task_id
        urlt="https://sbx.service-now.com/api/now/attachment/1232/file"
        user = "user"
        pwd = "sioxk"
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.patch(url=urlt+ tasknum, auth=(user,pwd), headers=headers ,data=payload)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            logging.debug('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
           # Decode the JSON response into a dictionary and use the data
        data = response.json()
        logging.debug(data)
        return "Success"
    except Exception as e:
        raise Exception(e)

