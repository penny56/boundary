'''
Created on July 29, 2022

@author: mayijie
'''

import sys, random
import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Global variables
host = "9.12.35.134"
cpc_name = "T257"
userid = "apiuser"
password = "apiuser"
verify_cert = False
part_props = {
    'name': 'boundary_newvNics',
    'ifl-processors': 1,
    'initial-memory': 1024,
    'maximum-memory': 1024,
}
vNic_name = "vNic_"
# will not failure when reach the max
vNic_max = 128


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
    
    print ("Creating a partition ...")
    part = None
    try:
        part = cpc.partitions.find_by_name(part_props["name"])
    except zhmcclient.NotFound:
        try:
            part = cpc.partitions.create(properties=part_props)
        except zhmcclient.Error as exc:
            print("Error: Cannot create partition {} on CPC {}: {}: {}".
                format(part_props["name"], cpc.name, exc.__class__.__name__, exc))
            raise

    print ("Current vNic number ...")
    vNic_curr = len(part.nics.list())
    print ("Current vNic number is {}, we need to create {} to reach the threshhold ...".
           format(str(vNic_curr), str(vNic_max-vNic_curr)))
    
    # Get the vSwitch
    vswitch = cpc.virtual_switches.findall(**{'type': 'osd'})[0]
    
    while (vNic_max-vNic_curr > 0):
        vNic_props = {'name' : vNic_name+str(random.randint(0,99999)),
                      'virtual-switch-uri' : vswitch.uri}
        try:
            part.nics.create(vNic_props)
        except zhmcclient.Error as exc:
            print("Error: Cannot create vNic {} on CPC {}: {}: {}".
                format(vNic_props["name"], cpc.name, exc.__class__.__name__, exc))
            raise
        vNic_curr += 1
    print ("Now we have " + str(vNic_max) + "vNics.")

finally:
    '''
    print("Deleting partition ...")
    if part != None:
        part.delete()
    '''
    print("Logging off ...")
    session.logoff()