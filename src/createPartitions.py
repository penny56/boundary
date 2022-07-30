'''
<SB10-7178-04a>
You can create as many partition definitions as you want, but only a specific number of partitions can be
active at any given time. The system limit determines the maximum number of concurrently active
partitions.

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
    'name': 'boundary_',
    'ifl-processors': 1,
    'initial-memory': 1024,
    'maximum-memory': 1024,
}
# will not failure when reach the max
part_max = 50



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
    
    print ("Current partition number ...")
    part_curr = len(cpc.partitions.list())
    print ("Current partition number is {}, we need to create {} to reach the threshhold ...".
           format(str(part_curr), str(part_max-part_curr)))

    while (part_max-part_curr > 0):
        try:
            part_props['name'] = 'boundary_' + str(random.randint(0,99999))
            try:
                part = cpc.partitions.create(properties=part_props)
            except zhmcclient.Error as exc:
                print("Error: Cannot create partition {} on CPC {}: {}: {}".
                    format(part_props["name"], cpc.name, exc.__class__.__name__, exc))
                raise
        except zhmcclient.Error as exc:
            print("Error: Cannot create partition {} on CPC {}: {}: {}".
                format(part_props["name"], cpc.name, exc.__class__.__name__, exc))
            raise
        part_curr += 1
    print ("Now we have " + str(part_max) + "partitions.")

finally:
    '''
    print("Deleting partition ...")
    if part != None:
        part.delete()
    '''
    print("Logging off ...")
    session.logoff()