'''
Created on Jul 16, 2020

@author: mayijie
'''

import zhmcclient
import time

class detachStorageGroup():
    
    @classmethod
    def start(cls, dpmObj):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        try:
            # Set boot option to 'None' before storage groups detached
            bootTempl = dict()
            bootTempl['boot-device'] = 'none'
            dpmObj.partition.update_properties(bootTempl)

            storageGroups = dpmObj.partition.list_attached_storage_groups()

            for storageGroup in storageGroups:
                dpmObj.partition.detach_storage_group(storageGroup)
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result

        time.sleep(1)
        
        result['success'] = True
        return result
 