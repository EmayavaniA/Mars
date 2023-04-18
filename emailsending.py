

import smtplib        

def sendmail():
    try:
        smtpServer='outlook.office365.com'      
        fromAddr='email.com'         
        toAddr='email1.com'     
        text= "This is a test of sending email from within Python."
        server = smtplib.SMTP(smtpServer,25)
        server.starttls()
        server.ehlo()
        server.login("email.com","123")
        result = server.sendmail(fromAddr, toAddr, text) 
        print(result)
        server.quit()
    except Exception as e:
        raise Exception(e)

sendmail()


---------------
import smtplib

# creates SMTP session
s = smtplib.SMTP('outlook.office365.com', 25)

# start TLS for security
s.starttls()

# Authentication
s.login("pp.com","AH")

# message to be sent
message = "Sample body"
# sending the mail
s.sendmail("email.com", "email.com", message)

# terminating the session
s.quit()
-----------------



'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = "email.com"
password = "123"
mail_from = "email.com"
mail_to = "email.com"
mail_subject = "Test Subject"
mail_body = "This is a test message"

mimemsg = MIMEMultipart()
mimemsg['From']=mail_from
mimemsg['To']=mail_to
mimemsg['Subject']=mail_subject
mimemsg.attach(MIMEText(mail_body, 'plain'))
connection = smtplib.SMTP(host='smtp.outlook.office.com', port=587)
connection.starttls()
connection.login(username,password)
connection.send_message(mimemsg)
connection.quit()'''
