'''
Created on Feb 2, 2019

@author: mayijie
'''

import zhmcclient
import time

class attachFICON():
    
    @classmethod
    def start(cls, dpmObj, ficonSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        cpcActiveFICONSgDict = dict()
        
        # Attach the storage group(s) and set the correct device number(s)
        try:
            cpcSgs = dpmObj.cpc.list_associated_storage_groups()
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result

        for cpcSg in cpcSgs:
            if cpcSg.get_property('type') == 'fc' and cpcSg.get_property('fulfillment-state') == 'complete':
                cpcActiveFICONSgDict[cpcSg.name] = cpcSg
        
        for sgName in eval(ficonSection['ficon_list']):
            # Check if the sgName exist in the cpc, the type is FICON and the state is complete
            if sgName in cpcActiveFICONSgDict.keys():
                try:
                    dpmObj.partition.attach_storage_group(cpcActiveFICONSgDict[sgName])
                except zhmcclient.HTTPError as e:
                    result['reason'] = e
                    return result
                time.sleep(1)
                
                # check if the attach action completed successfully
                try:
                    if len(cpcActiveFICONSgDict[sgName].list_attached_partitions(name = dpmObj.partition.get_property("name"))) != 1:
                        result['reason'] = "The storage group %s attached failed while checking after the attachment action!" % (sgName)
                        return result
                except zhmcclient.HTTPError:
                    result['reason'] = "List attached partitions for storage group %s action failed!" % (sgName)
                    return result
            else:
                result['reason'] = "The storage group %s is not exist or not in complete state!" % (sgName)
                return result
        time.sleep(1)
        
        result['success'] = True
        return result
 