from simple_salesforce import Salesforce
import requests
import pandas as pd
from io import StringIO
import logging
from configparser import ConfigParser
from datetime import datetime


def getLogger():
    LOG_FILENAME = datetime.now().strftime('logfile_%d_%m_%Y.log')
    logger = logging.basicConfig(filename='log_filename'+LOG_FILENAME,
             filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
             level=logging.DEBUG)
    return logger

logger = getLogger()

def getsfdcconnection():
    try:
        parser = ConfigParser()
        config_file_path = 'c:/path/db_config.ini'  # full absolute path here!
        parser.read(config_file_path)
        sf = {}
        if parser.has_section("sfdc"):
            items = parser.items("sfdc")
            for item in items:
                sf[item[0]] = item[1]
            #print(sf)
        else:
            logging.debug("Error in read ConfigParser")
            print("Error in read ConfigParser")
        sfdc_connection = Salesforce(username=sf['username'],password=sf['password'], security_token=sf['security_token'], domain=sf['domain'])
        if sfdc_connection:
            logging.info('SFDC Connection established.')
            #print('SFDC Connection established.')
        else:
            logging.info('SFDC Connection failed.')    
            #print('SFDC Connection failed.')
        return sfdc_connection  
    except Exception as e:
        raise Exception(e)

