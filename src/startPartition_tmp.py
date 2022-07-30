'''
Created on July 30, 2022

@author: mayijie
'''

import zhmcclient
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Global variables
host = "9.12.35.134"
cpc_name = "T257"
userid = "apiuser"
password = "apiuser"
verify_cert = False

part_name = "boundary_85972"

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
    
    print ("Find the partition ...")
    try:
        partition = cpc.partitions.find_by_name(part_name)
    except zhmcclient.NotFound:
        print("Error: Could not find partition {}".format(part_name))
        raise
    
    print ("Guarantee the partition is in stopped state ...")
    try:
        partition.wait_for_status(status="stopped", status_timeout=5)
    except zhmcclient.StatusTimeout as exc:
        print ("Failed! The partition not in Stopped state ...")
        print (exc)
        raise

    print ("Start the partition ...")
    try:
        partition.start(wait_for_completion = True, operation_timeout = 600, status_timeout = 600)
    except (zhmcclient.Error) as exc:
        print ("Failed! Start partition failed ....")
        print (exc)
        raise

    print ("done")

finally:
    '''
    print("Deleting partition ...")
    if part != None:
        part.delete()
    '''
    print("Logging off ...")
    session.logoff()