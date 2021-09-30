'''
Created on Feb 13, 2019

@author: mayijie
'''

import zhmcclient
import time

class setBootOption():
    
    @classmethod
    def start(cls, dpmObj, bootSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result

        if bootSection['boot_device'] != 'storage-volume':
            result['reason'] = "We couldn't set the boot option field for the partition not boot from SAN!"
            return result
        
        # construct the boot option template
        bootTempl = dict()
        bootTempl['boot-timeout'] = int(bootSection['boot-timeout'])
        
        # get the boot storage group uri
        try:
            sgObj = dpmObj.cpc.list_associated_storage_groups(filter_args={'name' : bootSection['storage_group_name']}).pop()
        except zhmcclient.NotFound:
            result['reason'] = "The storage group %s in the boot section not exist in the cpc!" % (bootSection['storage_group_name'])
            return result
        
        if sgObj.get_property("fulfillment-state") != "complete":
            result['reason'] = "The storage group %s in the boot section is not in complete state!" % (bootSection['storage_group_name'])
            return result

        if sgObj.get_property("type") == "fcp":
            svObjs = sgObj.storage_volumes.list(full_properties=True)
            for svObj in svObjs:
                if svObj.get_property("usage") == 'boot' and svObj.get_property("uuid") == bootSection['fcp-volume-uuid']:
                    bootTempl['boot-storage-volume'] = svObj.uri
                    bootTempl['boot-configuration-selector'] = int(bootSection['fcp-boot-configuration-selector'])
                    break
        elif sgObj.get_property("type") == "fc":
            # TODO for the boot from FICON
            pass
        else:
            pass
        
        try:
            dpmObj.partition.update_properties(bootTempl)
            bootTempl2 = dict()
            bootTempl2['boot-device'] = 'storage-volume'
            dpmObj.partition.update_properties(bootTempl2)
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result
        time.sleep(1)
        
        result['success'] = True
        return result