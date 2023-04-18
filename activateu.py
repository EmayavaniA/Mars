import requests, json
import var
import pandas as pd
from simple_salesforce import Salesforce
from gmail import send_mail_with_attachment
import os
import logging
import datetime
from snow import connect_snow_api_task_list, connect_snow_api_task_details, connect_snow_api_task_update

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

today_date = datetime.date.today()
today_date = str(today_date.strftime("%d-%m-%Y"))
file_path = dname+"/Update_Response_Files/"
file_name = "%s_User_Activate_list.xlsx" %(today_date)
log_file_name = dname + "/Moniter/%s_logfile.log" %(today_date)

logging.basicConfig(filename=log_file_name, format='%(asctime)s %(message)s', filemode='a',level=logging.INFO)
logging.info("------------Program Start-----------")

#--------------------Fetch Open request for Activation Account--------------------------

try:
    task_list_response = connect_snow_api_task_list(var.query_task_list)
    task_list_response = task_list_response.json()
    task_list=[]
    df = pd.DataFrame()

    for item in task_list_response["result"]["sc_task"]:
        temp = {}
        data_dir = {}
        sc_task = item["number"]
        task_details_response = connect_snow_api_task_details(sc_task)
        task_details_response = task_details_response.json()
        temp = {sc_task : task_details_response["result"]}

        if len(task_details_response["result"]["sc_task"]) and task_details_response["result"]["task_variables"][0]["hlr_AddRemoveUser"] == "Reactivate user":
            task_list.append(temp)
            data_dir = {"sc_task": sc_task,
                        "idf": task_details_response["result"]["sc_task"][0]["requested_for"],
                        "assigned_to": task_details_response["result"]["sc_task"][0]["assigned_to"]}

            df = df.append(data_dir,ignore_index=True)
        else:
            print(sc_task,task_details_response["result"]["task_variables"][0]["hlr_AddRemoveUser"])
    pass
except Exception as e:
    logging.info(str(e))


#-----------------Connect to SFDC---------------------------------

username_dev = var.username_dev
password_dev = var.password_dev
security_token_dev = var.security_token_dev
test = var.test

username_prod = var.username_prod
password_prod = var.password_prod
security_token_prod = var.security_token_prod


try:
    if test == "Y":
        sf = Salesforce(username=username_dev, password=password_dev, security_token=security_token_dev,
                        domain="test")
        logging.info("Connected to test Salesforce Successfully")
    elif test == "N":
        sf = Salesforce(username=username_prod, password=password_prod, security_token=security_token_prod,
                        domain="login")
        logging.info("Connected to prod Salesforce Successfully")

except Exception as e:
    logging.info("Error in connect to Salesforce:" + str(e))

#----------------------Fetch User Details from SFDC --------------------------------------

try:
    df_user = pd.DataFrame(columns=["sc_task","assigned_to","Id","Name","Username","","Country"])
    df_skip = pd.DataFrame(columns=["sc_task","assigned_to","Id","Name","Username","","Country","success","errors"])
    df_final = pd.DataFrame(columns=["sc_task","assigned_to","Id","Name","Username","","Country","success"])
    df_final_report = pd.DataFrame(columns=["sc_task", "Id", "Name", "Username", "", "Country", "success", "errors"])
    df_user_response = pd.DataFrame()
    query = var.query

    for index,row in df.iterrows():
        if row["FederationIdentifier"] != "":
            temp_query = query %(row["FederationIdentifier"])
            user_response = sf.bulk.User.query(temp_query)
            if len(user_response) > 0:
                df_user_response = pd.DataFrame(user_response)
                df_user_response["sc_task"] = row["sc_task"]
                df_user_response["assigned_to"] = row["assigned_to"]
                df_user = df_user.append(df_user_response)
            else:
                row["errors"] = "User_Id is incorrect or already in active state"
                row["success"] = False
                df_skip = df_skip.append(row,ignore_index=True)
        else:
            row["errors"] = "User_Id is blank in request"
            row["success"] = False
            df_skip = df_skip.append(row,ignore_index=True)

except Exception as e:
    logging.info("Error in fetching user details : " + str(e))

#-----------------------Update - User Activate ------------------------------

try:
    if len(df_user) > 0:
        df_user = df_user.reset_index(drop=True)
        df_user["IsActive"] = True
        df_upload = df_user[["Id","IsActive"]]
        dic_upload = df_upload.to_dict(orient='records')
        response = sf.bulk.user.update(dic_upload)
        final_res_df = pd.DataFrame(response)
        final_res_df = pd.concat([df_user, final_res_df], axis=1)
        df_final= final_res_df[["sc_task","assigned_to","Id","Name","Username","","Country","success","errors"]]

    df_final = df_final.append(df_skip,ignore_index=True)
    df_final = df_final.reset_index(drop=True)
    df_final["success"] = df_final["success"].astype(bool)
    pass
except Exception as e:
    logging.info("Error in User Update : " + str(e))



#------------Generate success error report--------------------
try:
    df_final_report = pd.DataFrame(columns=["sc_task","Id","Name","Username","","Country","success","errors"])
    if len(df_final) > 0:
        df_final_report = df_final[["sc_task","Id","Name","Username","","Country","success","errors"]]
        df_final = df_final.fillna("")
        df_final_report.to_excel(file_path+file_name)
        pass
except Exception as e:
    logging.info("Error in Generate success error report : " + str(e))

#--------------Close the sc_tasks-------------------
try:

    for index, row in df_final.iterrows():
        try:
            if row["success"] == True:
                connect_snow_api_task_update(row,True)
        except Exception as e:
            logging.info(row["sc_task"] + "Error in close the Sc task : " + str(e))
    pass
except Exception as e:
    logging.info("Error in close the ticket: " + str(e))

#---------------------Send email--------------------
try:
    status = ""
    df_all = pd.DataFrame(df_final_report["success"])
    df_true = df_all[df_all["success"] == True]
    print("len(df_all):" + str(len(df_all)) + " len(df_true): " + str(len(df_true)))
    if len(df_all) == len(df_true) and len(df_true) > 0:
        status = "Success"
    elif len(df_true) == 0 and len(df_all) > 0:
        status = "Failed"
    elif len(df_true) < len(df_all) and len(df_true) > 0:
        status = "Partial Complete"

    print("Status: " + status)
    if status != "":
        send_mail_with_attachment(status, file_name)
        logging.info("Mail sent")
        print("Mail sent")
    else:
        logging.info("No data to Update/sent mail")
    pass
except Exception as e:
    logging.info("Error in send email: " + str(e))

