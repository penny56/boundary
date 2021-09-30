'''
Created on Aug 26, 2019

@author: mayijie
'''

import zhmcclient
import time

class deletePartition():
    
    @classmethod
    def start(cls, dpmObj):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        # the status should be in stopped state before delete it
        try:
            dpmObj.partition.wait_for_status(status="stopped", status_timeout=5)
        except zhmcclient.StatusTimeout as e:
            result['reason'] = e
            return result
        
        # the status should be in active state before stop it
        try:
            dpmObj.partition.delete()
        except zhmcclient.StatusTimeout as e:
            result['reason'] = e
            return result
        
        time.sleep(1)
        result['success'] = True
        return result