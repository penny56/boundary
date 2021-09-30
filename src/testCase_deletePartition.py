'''
Created on Aug 26, 2019

20210930 Delete the partitions with the prefix name in [partition] section in config file

@author: mayijie
'''

import zhmcclient
import time

class deletePartition():
    
    @classmethod
    def start(cls, dpmObj, parSection):
        
        result = {'success': False, 'reason': ''}
        '''
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        # the status should be in stopped state before delete it
        try:
            dpmObj.partition.wait_for_status(status="stopped", status_timeout=5)
        except zhmcclient.StatusTimeout as e:
            result['reason'] = e
            return result
        '''
        
        try:
            parList = dpmObj.cpc.partitions.list()
        except Exception as e:
            result['reason'] = e
            return result
        print 
        for partition in parList:
            if parSection["par_name_prefix"] in str(partition.name):
                print "delete " + str(partition.name)
                # Deem that all the partitions in stopped state
                try:
                    partition.delete()
                except zhmcclient.StatusTimeout as e:
                    result['reason'] = e
                    return result

        time.sleep(1)
        result['success'] = True
        return result