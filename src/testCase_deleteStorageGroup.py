'''
Created on Jul 16, 2020

@author: mayijie
'''

import zhmcclient
import time

class deleteStorageGroup():
    
    @classmethod
    def start(cls, dpmObj, createSgSection):
        
        result = {'success': False, 'reason': ''}

        try:
            for cpcSg in dpmObj.cpc.list_associated_storage_groups():
                if str(cpcSg.get_property('name')) == createSgSection['sgname']:
                    # it's ok we don't supply the email address
                    cpcSg.delete()
                    break
            
            time.sleep(1)
            
            # check if the storage group no longer in the list
            for cpcSg in dpmObj.cpc.list_associated_storage_groups():
                if str(cpcSg.get_property('name')) == createSgSection['sgname']:
                    result['reason'] = "Deleted storage group still exist in cpc."
                    return result
        except Exception as e:
            result['reason'] = e
            return result

        time.sleep(1)
        result['success'] = True
        return result