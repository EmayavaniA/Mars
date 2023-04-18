import requests
from sys import exit


#url = 'https://xxx.service-now.com/api/now/table/sc_req_item?sysparm_query=Number%1DRITM11111&sysparm_limit=1'
#env = 'test'
user = 'admin'
pwd = 'admin'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

def toread_ritm():
    response = requests.get('http://11.111.111.111:443/t', auth=(user, pwd), headers=headers )
    # Check for HTTP codes other than 200
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    json_status = data['result']
    sys_id = data['result'][0][sys_id]
    # request body parms
    short_description = data['result'][0][short_description]
    error_msg = data['result'][0][error_msg]
    print(sys_id)
    print(error_msg)
    return sys_id
    exit()

