#This script is used to validate functionality of a FortiGate device. A sum of common controls and checks are done based on the available FortiGate API
#endpoints. This script is used to determining the current state of functioning.
#This script is validated on the following FortiGate(VM / FortiOS) firmware versions: 6.0.5, 6.2.0, 6.2.1

#Import the modules part of this script (these need to be installed on forehand via > pip install)
import requests
import time
import json
import os
from datetime import datetime

#Suppres anoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

#Import secrets
from secrets import *

#Get run time for identifying this session in the fortmat used is yyyymmdd-h00m00
now = datetime.now().strftime('%Y%m%d-h%Hm%M')

#Create folder structure for this itteration.
print('HealthCheck: Building folder tree structure in scipt directory: data/%s' %now )
path = os.path.dirname(os.path.realpath(__file__))
data = '/'.join ([ path, 'data' ])
datanow = '/'.join ([ path, 'data',now ])
if os.path.isdir(datanow) == False:
    os.makedirs(datanow)

#Functies welke gebruikt worden
def check_con():
    if r_sys.status_code == 200:
        print('HealthCheck: Retrieved data')
    elif r_sys.status_code != 200:
        print('HealthCheck [ERROR]: Could not retrieve data')
    return;

#Buidling blocks voor de get api endpoints
base_url = 'https://192.168.2.254:4443'
api_mon_int = '/api/v2/monitor/system/available-interfaces/select'
api_mon_rou = '/api/v2/monitor/router/ipv4/select'
api_mon_sys = '/api/v2/monitor/system/status/select'


#Bouw de urls op met de juiste API endpoints (vergeet de auth niet)
    #url_int is used for retrieving the available interface status and configurations
url_int = ''.join([base_url, api_mon_int, auth])
    #url_route is used for retrieving the IPv4 routing table information
url_route = ''.join([base_url, api_mon_rou, auth])
    #url_sys is used to retrieve system status information
url_sys = ''.join([base_url, api_mon_sys, auth])

#Retrieve data from FortiGate API endpoints
#export PYTHONWARNINGS = "ignore:Unverified HTTPS request"
#def int_req():
print('HealthCheck: Looking up system status')
r_sys = requests.get (url_sys, verify=False)
check_con()
#    return;

#int_req()
exit()

print('HealthCheck: Looking up interface data')
r_int = requests.get (url_int, verify=False)
check_con()

print('HealthCheck: Looking up routing table data')
r_rou = requests.get (url_route, verify=False)
check_con()

#Writing data to file archive
time.sleep(2)
f = open( '%s/system.txt' %datanow, 'w+' )
f.write(r_sys.text)
f.close
f = open( '%s/interface.txt' %datanow, 'w+' )
f.write(r_int.text)
f.close
f = open( '%s/routes.txt' %datanow, 'w+' )
f.write(r_rou.text)
f.close
