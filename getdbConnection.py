from mysql.connector import Error , MySQLConnection
import logging
from configparser import ConfigParser


def getdbConnection():
    try:
        parser = ConfigParser()
        config_file_path = 'c:/path/tp/db_config.ini'  # full absolute path here!
        parser.read(config_file_path)
        db = {}
        if parser.has_section("mysql"):
            items = parser.items("mysql")
            for item in items:
                db[item[0]] = item[1]
        else:
            logging.debug("Error in read ConfigParser")
            print("Error in read ConfigParser")
        connection = MySQLConnection(**db)
        if connection.is_connected():
            logging.info('Connection established.')
            print('Connection established.')
        else:
            logging.info('Connection failed.')    
            print('Connection failed.')
    except Exception as e:
        raise Exception(e)
    return connection 

def lookupfetch(short_desc):
    try:
        x= short_desc
        connection = getdbConnection()
        cursor = connection.cursor()
        sql1= """select * from lookuptest1 where Scriptmapping= (%s);"""
        cursor.execute(sql1,(x,))
        result1 = cursor.fetchone()
        rc = cursor.rowcount
        print("%d"%rc)
        if rc != -1:
            sql = """select Scriptname,Scriptpath from lookuptest1 where Scriptmapping= (%s);"""
            cursor.execute(sql,(x,))
            record = cursor.fetchone()
            Scriptname = record[0]
            Scriptpath = record[1]
            print("Scriptname is ", Scriptname)
            print("Scriptpath is ", Scriptpath) 
            return record
        else:
            print("No record found for ",x)
            #outputfailed= (None,None)
            return None
            
    except Exception as e:
        raise Exception(e)
     
usecasetype = "Activate"
lookupfetch(usecasetype)  
if (lookupfetch(usecasetype))!= None:
    x,y= lookupfetch(usecasetype)
    print(y+'\\'+x +" ")  

else:
    print("invalid Short Description")
  
'''finally:
            if connection is not None and connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")'''
