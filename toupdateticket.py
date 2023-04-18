import requests
import sys
from restapi_read import toread_ritm

# Set the request parameters
url = 'https://xxx.service-now.com/api/now/table/sc_req_item/'
#env = 'test'
user = 'admin'
pwd = 'admin'

# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}

# Do the HTTP request
def toupdateticket():
    ritm_sysid = toread_ritm()
    response = requests.patch(url=url+'ritm_sysid', auth=(user, pwd), headers=headers ,data="{\"u_resolution\":\"Closed\",\"u_comments_work_notes\":\"Ticket closed by python script\"}")
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
        exit()
    # Decode the JSON response into a dictionary and use the data
    data = response.json()
    print(data)
    exit()


toupdateticket()
