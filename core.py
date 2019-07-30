import requests

r = requests.get ('https://192.168.2.254:4443/api/v2/cmdb/system/interface?format=name&access_token=rzktp5dn7915qqy3yqrswnyc3qrGdh', verify=False)
print(r.text)
