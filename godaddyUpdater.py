import requests
import json
import argparse
import os
from dotenv import load_dotenv

parser = argparse.ArgumentParser(description='App for changing IP address of godaddy domains')
parser.add_argument('domain_name', type=str, help='domain name to be changed')
args = parser.parse_args()

load_dotenv()

key = os.getenv('GODADDY_KEY')
secret = os.getenv('GODADDY_SECRET')

domain = args.domain_name

dns_record_type = 'A' #change this if you want to update 
dns_record_name = '@' #other record types / names
 
headers_get_domaininfo = {"Authorization" : "sso-key {}:{}".format(key, secret)}
headers_set_domaininfo = {"Authorization" : "sso-key {}:{}".format(key, secret), "accept": "application/json", "Content-Type": "application/json"}
url = "https://api.godaddy.com/v1/domains/{}/records/{}/{}".format(domain,dns_record_type,dns_record_name)


current_ip = requests.get('https://api.ipify.org').text

r = requests.get(url,  headers=headers_get_domaininfo)
r_json = json.loads(r.text)
godaddy_ip = r_json[0]['data']
print('My public IP address is: {}, {} IP is {}'.format(current_ip, domain, godaddy_ip))

update_template = [{
    "data": current_ip,
    "name": "@",
    "port": 65535,
    "priority": 0,
    "service": "string",
    "ttl": 3600,
    "type": "A",
    "weight": 1
    }]
    
payload = json.dumps(update_template)  


def update_ip():
    print("Changing ip on {} to {}...".format(domain, current_ip))
    p = requests.put(url, headers=headers_set_domaininfo, data=payload)
    if p.status_code == 200:
        print("Success!")
    else:
        print("Request failed")

if current_ip != godaddy_ip:
    print("IP address is different, changing ip")
    update_ip()
else:
    print("IP address is equal, bailing out")
    

