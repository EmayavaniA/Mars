import os
import logging
from simple_salesforce import Salesforce
from datetime import datetime
import pandas as pd 
from flask import Flask, jsonify, request
import requests
import json
import ast
import base64


def getLogger(file_name):
    LOG_FILENAME = datetime.now().strftime('_%d_%m_%Y.log')
    logpath= "Logs"
    if not os.path.exists("Logs"):
        os.makedirs("Logs")
    logger = logging.basicConfig( filename =logpath+"//"+file_name+LOG_FILENAME,
             filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
             level=logging.DEBUG)
    return logger

def getsfdcconnection():
    try:
        username="email.com"
        password="ppp"
        security_token="sfggr22"
        domain="test"
        sfdc_connection = Salesforce(username=username,password=password, security_token=security_token, domain=domain)
        if sfdc_connection:
            logging.info('SFDC Connection established.')
            return sfdc_connection  
        else:
            logging.error('SFDC Connection failed.')    
            return sfdc_connection  
    except Exception as e:
        logging.error(e)
        raise Exception(e)
        
    
def decodingAttacthment(encodedattatchment):
    try:
        decodefile = encodedattatchment
        if decodefile is not None:
            message_bytes = (base64.b64decode(decodefile))
            data=str(message_bytes,'utf-8')
            a3=ast.literal_eval(data)
            return a3
        else:
            return None
    except Exception as e:
        logging.error(e)
        raise Exception(e)
    
def removet(li):
    li=[ num for num in li if num]
    return li
   
def updatetask1(task_id,payloaddata):
    try:
        payload = json.dumps(payloaddata)
        #payload = (payloaddata)
        tasknum = task_id
        urlt="https://xxx.service-now.com/api/now/table/sc_task/"
        user = "xxa\username.com"
        pwd = "xxxx"
        headers = {"Content-Type":"application/json","Accept":"application/json"}
        response = requests.patch(url=urlt+ tasknum, auth=(user,pwd), headers=headers ,data=payload)
        # Check for HTTP codes other than 200
        if response.status_code != 200:
            logging.info('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
           # Decode the JSON response into a dictionary and use the data
        data = response.json()
        logging.info(data)
        return "Success"
    except Exception as e:
        logging.error(e)
        raise Exception(e)

def updatetask(task_id,payloaddata):
    try:
        payload = json.dumps(payloaddata)
        print(payload)
        tasknum = task_id
        logging.info(tasknum)
    except Exception as e:
        logging.error(e)
        raise Exception(e)
