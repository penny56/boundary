'''
Created on Feb 8, 2019

@author: mayijie
'''

import zhmcclient
import time

# new a accelerator virtual function for the partition
class newAccelerator():
    
    @classmethod
    def start(cls, dpmObj, acceleratorSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        acceList = eval(acceleratorSection['acce_list'])
        for acceDict in acceList:
            # get the adapter uri
            try:
                adapter = dpmObj.cpc.adapters.find(name = acceDict['adapter-name'])
            except zhmcclient.NotFound as e:
                result['reason'] = e
                return result
            
            # construct the virtual function template
            acceTempl = dict()
            acceTempl["name"] = acceDict["name"]
            acceTempl["adapter-uri"] = adapter.get_property("object-uri")
            
            # for the optional options
            if "description" in acceDict.keys():
                acceTempl["description"] = acceDict["description"]
            if "device-number" in acceDict.keys():
                acceTempl["device-number"] = acceDict["device-number"]
            
            try:
                dpmObj.partition.virtual_functions.create(acceTempl)
            except zhmcclient.HTTPError as e:
                result['reason'] = e
                return result
            time.sleep(1)
            
            # check the accelerator exists
            try:
                dpmObj.partition.virtual_functions.find(name = acceDict["name"])
            except zhmcclient.NotFound as e:
                result['reason'] = e
                return result
        time.sleep(1)
        
        result['success'] = True
        return result