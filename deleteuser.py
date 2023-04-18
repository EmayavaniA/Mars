from simple_salesforce import Salesforce
import pandas as pd
import datetime
import os
import logging
from gmail import send_single_mail
import datetime
import var

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

today_date = datetime.date.today()
today_date = str(today_date.strftime("%d-%m-%Y"))

file_path = dname+"/Deactivate_list/"
file_name = "%s_Deactivate_list.xlsx" %(today_date)
log_file_name = dname + "/Moniter/%s_logfile.log" %(today_date)

logging.basicConfig(filename=log_file_name, format='%(asctime)s %(message)s', filemode='a',level=logging.INFO)
logging.info("------------Program Start-----------")


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

try:
    query_audit = var.query_audit
    result = sf.bulk.SetupAuditTrail.query(query_audit)
    df_audit = pd.DataFrame(result)
    df_audit = df_audit.fillna('')
    audit_list = []
    for item in df_audit['Display']:
        temp = item.split("(UserID: [")
        temp2 = temp[1].split("]")
        user_id = temp2[0]
        audit_list.append(user_id)

    audit_list = tuple(audit_list)

except Exception as e:
    logging.info("Error in fetching user list: " + str(e))

query = var.query.format(audit_list)

try:
    result = sf.bulk.user.query(query)
    df_user = pd.DataFrame(result)
    df_user = df_user.fillna('')

except Exception as e:
    logging.info("Error in fetching user list: " + str(e))

#-------------------------Calculate Deactivation Date & Remaining Days ---------------------------

try:
    df_user["Deactivation_Date"] = ""
    df_user["Remaining_Days"] = ""
    today_now = datetime.datetime.now().date()
    d = datetime.timedelta(days=90)
    for index, row in df_user.iterrows():
        if row["LastLoginDate"] != "":
            temp_date_str= row["LastLoginDate"]
        else:
            temp_date_str = row["CreatedDate"]

        #temp_date = datetime.datetime.strptime(temp_date_str, "%m/%d/%Y, %I:%M %p").date()
        temp_date = datetime.datetime.strptime(temp_date_str, "%d.%m.%Y, %H:%M").date()
        deactivation_date = temp_date + d
        remainig_days = (deactivation_date - today_now).days
        print("Deactivation Date: " + str(deactivation_date), "Remaining Days: " + str(remainig_days))
        df_user["Deactivation_Date"][index] = str(deactivation_date.strftime("%d-%m-%Y"))
        df_user["Remaining_Days"][index] = remainig_days

    df_user.to_excel(file_path+file_name)

    pass
except Exception as e:
    logging.info("Error in calculating deactivate time: " + str(e))

#-----------------------Send Mail --------------------------------------

try:
    # df_user["Email"] = "harshkumar.vekariya@contractors.roche.com"

    for index, row in df_user.iterrows():
        try:
            if row["Remaining_Days"] in [10,7,5,3,2,1]:
                send_single_mail(row)
        except Exception as e:
            logging.info("Error in sending mail to : " + str(row['Email']) + "  " + str(e))

except Exception as e:
    logging.info("Error in sending mail : " + str(e))

logging.info("-------------------Complete the Program----------------")
