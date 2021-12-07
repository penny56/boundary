'''
Created on Feb 14, 2019

@author: mayijie
'''

import zhmcclient
import time

class startPartition():
    
    @classmethod
    def start(cls, dpmObj):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        # the status should be in stopped state before start it
        try:
            dpmObj.partition.wait_for_status(status="stopped", status_timeout=5)
        except zhmcclient.StatusTimeout as e:
            result['reason'] = e
            return result
        
        # the boot option should be boot from SAN, otherwise, start partition fail
        try:
            if dpmObj.partition.get_property('boot-device') != 'storage-volume':
                result['reason'] = "Partition should boot from SAN before start."
                return result
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result
        '''
        try:
            # Here we don't wait for the operation complete, check up the status later
            dpmObj.partition.start(wait_for_completion=False)
        except (zhmcclient.HTTPError, Exception) as e:
            result['reason'] = e
            return result
        time.sleep(10)
        
        # check up the status, time out = 5mins, and return immediately after enter active state.
        try:
            dpmObj.partition.wait_for_status(status="active", status_timeout=300)
        except zhmcclient.StatusTimeout as e:
            result['reason'] = e
            return result
        '''
        # wait for completion of the asynchronous job performing the operation 
        start = int(time.time())
        try:
            dpmObj.partition.start(wait_for_completion = True, operation_timeout = 600, status_timeout = 600)
        except (zhmcclient.HTTPError, Exception) as e:
            result['reason'] = e
            return result
        end = int(time.time())
        print ("starting time span is: " + str(end - start))
        
        time.sleep(10)
        result['success'] = True
        return result