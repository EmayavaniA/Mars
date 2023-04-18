from simple_salesforce import Salesforce
import pandas as pd

sfdc_connection = Salesforce(username='aaa',password='xxx', security_token='adss12f', domain='test')
sql_1 = "select columns from object where username = 'email.com' "
results=sfdc_connection.query_all(sql_1)
if len(results['records'])>0:
    print("Query_records=",results)
    df = pd.DataFrame(results['records']).drop(columns='attributes')
    print(df)
    x= df['Id']
    print(x)
    print(x.values[0])
    y=df['IsActive'].values[0]
    print(y)

