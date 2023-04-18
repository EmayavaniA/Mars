username_dev = "test@gmail.com"
password_dev = "123"
security_token_dev = "123"
test = "N"

username_prod = "test@das.sda"
password_prod = "123"
security_token_prod = '123'

query_audit = "SELECT Display from SetupAuditTrail where action like 'activateduser' and createddate = LAST_N_DAYS:14"

query = """	Select 																	        
                id,
                UserName,
                Email,
                Roche_User_ID__c,
                FederationIdentifier,
                Name,Profile.Name,
                FORMAT(LastLoginDate),
                FORMAT(CreatedDate),
                FORMAT(LastModifiedDate),
                UserRole.Name,
                IsActive,
                Country 
                    from 
                        User 
                    where 
                profileId in (select id from profile 
                where Name in ('')) 
                and isActive = True and Prevent_Deactivation__c = False 
                and (LastLoginDate < LAST_N_DAYS:75 OR (LastLoginDate=null AND CreatedDate < LAST_N_DAYS:75))
                and id not in {}
                order by 
                LastLoginDate Desc 
        """


server='smtp.gmail.com'
port = 465

gmail_user = 'test@gmail.com'
gmail_password = '123'
send_from = "test@gmail.com"
send_to = ["test@gmail.com"]
subject = "Reminder of Salesforce User ID Deactivation - %s"
text = """Hi %s, <br><br>
    This is gentle reminder.<br><br>
    Your Id will be deactivated on %s (in<b style="color:red"> %s days</b>).<br><br>
    Username : <b>%s</b><br><br>
    Please <a href="https://salesforce.com/">login</a> to your account to avoid deactivate your license.<br><br> 
    <b><i>Thanks  & Regards<br>
    Automation Team</i></b>
    """

file_path = "C:/Users/%s"
