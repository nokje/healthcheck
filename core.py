#This script is used to validate functionality of a FortiGate device. A sum of common controls and checks are done based on the available FortiGate API
#endpoints. This script is used to determining the current state of functioning.
#This script is validated on the following FortiGate(VM / FortiOS) firmware versions: 6.0.5, 6.2.0, 6.2.1


#TODO list
# Validate -p value (port range)

#Import the modules part of this script (these may be needing manual installation via > pip install)
import requests, time, json, os, sys, argparse, socket
from datetime import datetime

#Check if the correct argument is added to the call.
parser = argparse.ArgumentParser(description='This script is used to validate functionality of a FortiGate device. A sum of common controls and checks are done based on the available FortiGate API endpoints. It stores how the FortiGate functions. This script has been tested on the following FortiGate(VM / FortiOS) firmware versions: 6.0.5, 6.2.0, 6.2.1')
parser.add_argument("IP_ADDR", help="Enter the IP address of the FortiGate firewall")
parser.add_argument("-p", help="Range = 1-65535. To use a different portnumber for the FortiGate adminportal. (default = 443)")
args = parser.parse_args()

#Check if the given IP address is a valid IPv4 address.
try:
    socket.inet_aton(args.IP_ADDR)
except socket.error:
    print('HealthCheck [%s]: The IP address is not a valid IPv4 address.' %run_id)
    exit(1)

#Check if the -p option contains a valid port number.
#if args.p in range(1,65535):
#   print( " %s is in the range"%str(n))
#else :
#   print('HealthCheck [%s]: The given portnumber is outside the TCP portrange (1-65535).' %run_id)
#   exit(1)

#Suppres anoying InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

#Import secrets
from secrets import *

#Get run time for identifying this session. The session identifier is 'yyyymmdd-h00m00' format.
run_id = datetime.now().strftime('%Y%m%d-h%Hm%M')
print('HealthCheck [%s]: Starting HealthCheck session.' %run_id)

#Create folder structure for this itteration.
path = os.path.dirname(os.path.realpath(__file__))
data_run = '/'.join ([ path, 'data',run_id ])
if os.path.isdir(data_run) == False:
    os.makedirs(data_run)

#Function to cURL the data
def req_data( end_point, file_name ):
    if args.p == None:
        req_url = ''.join(['https://', args.IP_ADDR, end_point, auth])
    else:
        req_url = ''.join(['https://', args.IP_ADDR,':', args.p, end_point, auth])
    try:
        query = requests.get ( req_url, verify = False )
    except requests.ConnectionError, e:
        print(e), exit(1)
    sys.stdout = open( '/'.join([data_run, file_name]), 'w+' )
    print(query.text)
    return;

print('HealthCheck [%s]: Acquired the data and stored it in my ./data folder.' %run_id )
req_data( end_point = '/api/v2/monitor/system/available-interfaces/select', file_name = 'interface.txt' )
req_data( end_point = '/api/v2/monitor/router/ipv4/select', file_name = 'routes.txt' )
req_data( end_point = '/api/v2/monitor/system/status/select', file_name = 'system.txt' )

print('HealthCheck [%s]: Script finished its run.' %run_id )
