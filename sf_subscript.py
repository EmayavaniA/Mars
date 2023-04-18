import json
import pandas as pd
from pyfunctions import *
from pycontroller import *


Json_received = json.loads(sys.argv[1])
short_desc = Json_received["UseCaseType"]
task_id = Json_received["CatalogTaskNo"]
ritm = Json_received["RITM_No"]
logfilename = short_desc +"_"+ str(ritm)
logger = getLogger(logfilename)
sys_id =Json_received["sys_id_CatalogTask"]
attatchmnet = Json_received["AttachmentData"]
datalist= decodingAttacthment(attatchmnet)
logging.info("Hey setupdate script has opened")
#logging.info(datalist)
#logging.info ("Number of arguments:", len(sys.argv), "arguments")
#logging.info ("Argument List:", str(sys.argv[1]))


			
def SSkeylookuptlookup(SS_keyrequested):
    try:
        SS_key = SS_keyrequested
        if SS_key == "Generic SS":
            SS_Name = "ATS_High_Volume"
            return SS_Name
        elif SS_key == "Access to Export Excel":
            SS_Name = "SS__Export"
            return SS_Name
        elif SS_key == "Access to create report":
            SS_Name = "SS__Creation"
            return SS_Name
        elif SS_key == "For Singapore":
            SS_Name = "SS_Singapore"
            return SS_Name
        elif SS_key == "Access to Public Dashboard":
            SS_Name = "SS_Access"
            return SS_Name
        else:
            logging.error("NO record found for ",SS_key)
    except Exception as e:
        logging.error(e)
        raise Exception(e)


def toactivateuser(userdf):
    try:
        sfconnection = getsfdcconnection()
        logging.info("Inside try to activate")
        df=userdf
        df['IsActive']=True
        df["set_Sets__c"]= 'bh'
        dict_records = df.to_dict('records')
        logging.info(dict_records)
        user_activated=sfconnection.bulk.User.update(dict_records)
        logging.info(user_activated)
    except Exception as e:
        logging.error(e)
        raise Exception(e)

def sfdcgetuserID(user_email):
    try:
        u_mail=user_email
        sfconnection = getsfdcconnection()
        soql_1 = " select username ,Id, IsActive from user where email = '" + u_mail + "' "
        results=sfconnection.query_all(soql_1)
        if len(results['records'])>0:
            df = pd.DataFrame(results['records']).drop(columns='attributes')
            if (df['IsActive'] == False).any():
                df=toactivateuser(df)
            userid=df['Id'].values[0]
            return userid
        else:
          logging.error("New user/Invalid user ", user_email)
          return None
    except Exception as e:
        logging.error(e)
        raise Exception(e)
    
def mimicset(ref_user_id,requested_userID):
    try:
        sfconnection = getsfdcconnection()
        requested_id = sfdcgetuserID(requested_userID)
        reference_user = sfdcgetuserID(ref_user_id)
        logging.info("Inside Mimic function with ref user ",ref_user_id +" and req user " ,requested_userID)
        if (requested_id is not None) and (reference_user is not None): 
            soql_SELECT = "select Id,AssigneeId,setId from setAssignment where AssigneeId ='" + str(reference_user) + "'"
            results5=sfconnection.query_all(soql_SELECT)
            if len(results5['records'])>0:
                df3 = pd.DataFrame(results5['records']).drop(columns='attributes')
                #logging.info("df3 =",df3)
                df3["AssigneeId"]= requested_id
                df4=df3.drop(['Id'], axis=1)
                #logging.info("df4 =",df4)
                dict_records = df4.to_dict('records')
                #logging.info(type(dict_records))
                #logging.info(dict_records)
                for i in range(len(dict_records)):
                    requested_userIDlist = dict_records[i]["AssigneeId"]
                    setIdlist = dict_records[i]["setId"]
                    soql_SELECT = "select Id,AssigneeId,setId from setAssignment where AssigneeId ='" + str(requested_userIDlist) + "' and setId = '"+str(setIdlist)+"'"
                    results3=sfconnection.query_all(soql_SELECT)
                    if len(results3['records'])==0:
                        #logging.info("--"  *30)
                        #logging.info(dict_records[i])
                        df_add={'AssigneeId':''+str(requested_userIDlist)+'','setId':''+str(setIdlist)+''}  
                        #logging.info(df_add)
                        set_setCREATED=sfconnection.setAssignment.create(df_add)
                        logging.info(set_setCREATED)
                        mimic_success="sets has been created for the user",requested_userID
                        logging.info(mimic_success)
                        return mimic_success,True
                    else:
                        logging.info(results3)
                        mimic_failure="sets are already available for the user",requested_userID
                        logging.info(mimic_failure)
                        return mimic_failure,True
            else:
                mimic_failurea="No given set found for the Reference user",requested_userID
                logging.info(mimic_failurea)
                return mimic_failurea,False
        else:
            mimic_failureb="invalid the user" ,requested_userID,' or ref_user', requested_userID
            logging.error(mimic_failureb)
            return mimic_failureb,False      
    except Exception as e:
        logging.error(e)
        raise Exception(e)
    
def deleteset(useremail_id,SS_list):
    try:
        sfconnection = getsfdcconnection()
        Assignee_id = sfdcgetuserID(useremail_id)
        set_id =SSlookuptlookup(SS_list) 
        logging.info("Inside Delete function with user ",useremail_id + " and SS ",SS_list)
        if (Assignee_id is not None) and (set_id is not None): 
            sql_del = "select Id,AssigneeId,setId from setAssignment where setId ='" + str(set_id) + "' and AssigneeId ='" + str(Assignee_id) + "'"
            results3=sfconnection.query_all(sql_del)
            if len(results3['records'])>0:
                #logging.info("Query_records=",results3)
                df3 = pd.DataFrame(results3['records']).drop(columns='attributes')
                #logging.info(df3['Id'].values[0])
                ID = df3['Id'].values[0]
                set_setdelete=sfconnection.setAssignment.delete(ID)
                #logging.info(set_setdelete)
                delete_success="The given set ",SS_list," has been deleted for the user",useremail_id
                logging.info(delete_success)
                return delete_success,True
            else:
                delete_failurea=SS_list,"The set is not available to the user",useremail_id
                logging.info(delete_failurea)
                return delete_failurea,True
        else:
            delete_failure="invalid the user" ,useremail_id,' or set', SS_list
            logging.error(delete_failure)
            return delete_failure,False     
    except Exception as e:
        logging.error(e)
        raise Exception(e)
    
def addset(useremail_id,SS_list):
    try:
        sfconnection = getsfdcconnection()
        assignee_id = sfdcgetuserID(useremail_id)
        set_Id =SSlookuptlookup(SS_list) 
        logging.info("Inside ADD SS function with user ",useremail_id + " and SS ",SS_list)
        if (assignee_id is not None) and (set_Id is not None):  
            soql_SELECT = "select Id,AssigneeId,setId from setAssignment where AssigneeId ='" + str(assignee_id) + "' and setId ='"+ str(set_Id) +"'"
            results=sfconnection.query_all(soql_SELECT)
            if len(results['records'])==0:
                df_add = pd.DataFrame(results['records'])
                df_add={'AssigneeId':''+str(assignee_id)+'','setId':''+str(set_Id)+''}    
                #logging.info(df_add)
                set_add=sfconnection.setAssignment.create(df_add)
                logging.info(set_add)
                add_success = 'The given set',SS_list, "has been added for the user",useremail_id
                logging.info(add_success)
                return add_success,True
            else:
                add_Failure = SS_list," set is alredy avilable to the user"
                logging.info(add_Failure)
                return add_Failure,True
        else:
            add_Failurea = "invalid the user" ,useremail_id,' or set', SS_list
            logging.error(add_Failurea)
            return add_Failurea,False
    except Exception as e:
        logging.error(e)
        raise Exception(e)


if datalist is not None:
    pay_x=()
    pay_x_t=()
    for i in range(len(datalist)):
        Email = datalist[i]["Email"]
        ref_email = datalist[i]["Reference Email"]
        add_remove= datalist[i]["ADD/DELETE SS"]
        SS1= [datalist[i]["1"],datalist[i]["2"], datalist[i]["3"],datalist[i]["4"] ,datalist[i]["5"],datalist[i]["6"],datalist[i]["7"] ,datalist[i][" 8"],datalist[i]["9"],datalist[i]["10"]]
        SS_lists = list(filter(None, SS1))
        SSkey= [datalist[i][" 1"],datalist[i][" 2"], datalist[i][" 3"],datalist[i][" 4"] ,datalist[i][" 5"]]
        SSkey_lists = list(filter(None, SSkey))
        addres=()
        delres=()
        mimres=()
        t_addres=()
        t_delres=()
        t_mimres=()
        t_addresl=()
        t_delresl=()
        addresl=()
        delresl=()
        if (add_remove == "ADD") and (SSkey_lists != None):
                for b in SSkey_lists:
                    SS_name = SSkeylookuptlookup(b)
                    c,d=addset(Email,SS_name)
                    if d==True:
                      t_addresl = t_addresl+ (d,)
                    else:
                      addresl = addresl+ (c,)
        elif (add_remove == "Delete") and (SSkey_lists != None):
                for b in SSkey_lists:
                    SS_name = SSkeylookuptlookup(b)
                    u,v=deleteset(Email,SS_name)
                    if v==True:
                      t_delresl = t_delresl+ (v,)
                    else:
                      delresl = delresl+ (u,)
        if (add_remove == "ADD") and (SS_lists != None):
                for a in SS_lists:
                  m,n=addset(Email,a)
                  if n==True:
                    t_addres = t_addres+ (n,)
                  else:
                    addres = addres+ (m,)
        elif (add_remove == "Delete") and (SS_lists != None):
                for a in SS_lists:
                  p,q=deleteset(Email,a)
                  if q==True:
                        t_delres = t_delres+ (q,)
                  else:
                    delres = delres+ (p,)
        elif (add_remove == "Mimic") and (ref_email is not None): 
                r,s=mimicset(ref_email,Email)
                if s==True:
                    t_mimres = t_mimres+ (s,)
                else:
                    mimres = mimres+ (r,)
        else:
            attatchment_err= "Not a valid option selected for '"'ADD/DELETE SS'"' column"
            pay_laodatt= {"state": 8, "close_notes":attatchment_err}
        final =addres+delres+mimres+addresl+delresl
        pay_x=pay_x+(final,)
        final_t =t_addres+t_delres+t_mimres+t_addresl+t_delresl
        pay_x_t=pay_x_t+(final_t,)
    pay_xt =removet(pay_x_t)
    res_t=all(pay_xt)
    if res_t == True:
        pay_laodatt= {"state": 3, "close_notes":"Request has been completed by bot"}
    else:
        tup = removet(pay_x)
        strings =','.join(str(v) for v in tup)
        logging.info("s=",strings)
        pay_laodatt = {"state": 8, "close_notes": strings}
    updatetask(task_id,pay_laodatt)
else:
    attatchment_error= "No attatchment found"
    logging.info(attatchment_error)
    pay_laodatta= {"state": 8, "close_notes":attatchment_error}
    updatetask(task_id,pay_laodatta)
    sys.exit(0)

