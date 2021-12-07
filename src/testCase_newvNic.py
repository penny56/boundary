'''
Created on Nov 19, 2021

@author: mayijie
'''

import zhmcclient
import time

# for OSA only, for RoCE, please reference the doc
class newvNic():
    
    @classmethod
    def start(cls, dpmObj, vnicSection):
        
        result = {'success': False, 'reason': ''}
        
        # Check if the partition exist.
        try:
            partition = dpmObj.cpc.partitions.find(name = vnicSection["part_name"])
        except zhmcclient.NotFound as e:
                result['reason'] = e
                return result

        # Check if the adapter exist.
        try:
            # Please note here ::: here you can use name = vnicSection["adapter_name"] as the find() parameter
            # but you can NOT use adapter-id = vnicSection["adapter_id"] as the find() parameter
            # Because they deem the '-' is an expression! Make no sense! 
            # One way you can use the name = vnicSection["adapter_name"]
            # The other way is use find(**{}), like now we are using
            
            #adapter = dpmObj.cpc.adapters.find(name = vnicSection["adapter_name"])
            adapter = dpmObj.cpc.adapters.find(**{'adapter-id': vnicSection["adapter_id"]})
        except zhmcclient.NotFound as e:
            result['reason'] = e
            return result
    
        # Get the vSwitch
        vswitches = dpmObj.cpc.virtual_switches.findall(**{'backing-adapter-uri': adapter.uri})
        vswitch = None
        for vs in vswitches:
            if vs.get_property('port') == int(vnicSection["adapter_port"]):
                vswitch = vs
                break
    
        # Construct the vNic template
        vnicTempl = dict()
        vnicTempl["name"] = vnicSection["vnic_name_prefix"]
        vnicTempl["virtual-switch-uri"] = vswitch.uri
    
        # Create the vNic
        try:
            new_vnic = partition.nics.create(vnicTempl)
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result
        time.sleep(1)
    
        # Check if the vNic exist
        ''' NO need to check
        try:
            partition.nics.find(name = vnicTempl["name"])
        except zhmcclient.NotFound as e:
            result['reason'] = e
            return result
        '''
        time.sleep(1)
        result['success'] = True
        return result