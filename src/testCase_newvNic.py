'''
Created on Jan 15, 2019

@author: mayijie
'''

import zhmcclient
import time

# for OSA only, for RoCE, please reference the doc
class newvNic():
    
    @classmethod
    def start(cls, dpmObj, vnicSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        vnicList = eval(vnicSection['vnic_list'])

        for vnicDict in vnicList:
            # Check if the adapter exist.
            try:
                adapter = dpmObj.cpc.adapters.find(name = vnicDict["adaptername"])
            except zhmcclient.NotFound as e:
                result['reason'] = e
                return result
        
            # Get the vSwitch
            vswitches = dpmObj.cpc.virtual_switches.findall(**{'backing-adapter-uri': adapter.uri})
            vswitch = None
            for vs in vswitches:
                if vs.get_property('port') == int(vnicDict["adapterport"]):
                    vswitch = vs
                    break
        
            # Construct the vNic template
            vnicTempl = dict()
            vnicTempl["name"] = vnicDict["vnicname"]
            vnicTempl["description"] = vnicDict["vnicdesc"]
            vnicTempl["device-number"] = vnicDict["vnicdevnum"]
            vnicTempl["virtual-switch-uri"] = vswitch.uri
        
            # Create the vNic
            try:
                new_vnic = dpmObj.partition.nics.create(vnicTempl)
            except zhmcclient.HTTPError as e:
                result['reason'] = e
                return result
            time.sleep(1)
        
            # Check if the vNic exist
            try:
                dpmObj.partition.nics.find(name = vnicTempl["name"])
            except zhmcclient.NotFound as e:
                result['reason'] = e
                return result
            time.sleep(1)
        
        result['success'] = True
        return result