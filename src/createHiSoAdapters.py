'''
Created on Aug. 01, 2022

@author: mayijie
'''

import random
import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Global variables
host = "9.12.35.134"
cpc_name = "T257"
userid = "apiuser"
password = "apiuser"
verify_cert = False

hiSo_props = {}
# will not failure when reach the max
hiSo_max = 32


print("Using HMC {} system {} with userid {} ...".format(host, cpc_name, userid))

print("Creating a session with the HMC ...")
try:
    session = zhmcclient.Session(host, userid, password, verify_cert=verify_cert)
except zhmcclient.Error as exc:
    print("Error: Cannot establish session with HMC {}: {}: {}".format(host, exc.__class__.__name__, exc))


try:
    client = zhmcclient.Client(session)
    
    print ("Find the cpc ...")
    try:
        cpc = client.cpcs.find(name=cpc_name)
    except zhmcclient.NotFound:
        print("Error: Could not find CPC {}".format(cpc_name))
        raise

    print ("Current hiSo number ...")
    hiSo_curr = len(cpc.adapters.list(filter_args={'type': 'hipersockets'}))
    print ("Current hiSo adapters number is {}, we need to create {} to reach the threshhold ...".
           format(str(hiSo_curr), str(hiSo_max-hiSo_curr)))

    while (hiSo_max-hiSo_curr > 0):
        hiSo_props['name'] = 'hiSo_' + str(random.randint(0,99999))
        try:
            new_adapter = cpc.adapters.create_hipersocket(hiSo_props)
        except zhmcclient.Error as exc:
            print("Error: Cannot create hipersocket Adapter {} on CPC {}: {}: {}".
                format(hiSo_props['name'], cpc.name, exc.__class__.__name__, exc))
            raise
        hiSo_curr += 1
    print ("Now we have " + str(hiSo_max) + " hipersocket adapter.")

finally:
    print("Logging off ...")
    session.logoff()