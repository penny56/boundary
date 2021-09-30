'''
Created on Feb 10, 2019

@author: mayijie
'''

import zhmcclient
import time

# new a accelerator virtual function for the partition
class addCrypto():
    
    @classmethod
    def start(cls, dpmObj, cryptoSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        crypto_domain = eval(cryptoSection['crypto_domain'])
        if len(crypto_domain) > 0:
            adapterNameList = crypto_domain.pop('crypto-adapter-names')
            adapters = []
            
            for adapterName in adapterNameList:
                try:
                    adapter = dpmObj.cpc.adapters.find(name = adapterName)
                except zhmcclient.NotFound as e:
                    result['reason'] = e
                    return result
                adapters.append(adapter)
            
            try:
                dpmObj.partition.increase_crypto_config(adapters, crypto_domain['crypto-domain-configurations'])
            except zhmcclient.HTTPError as e:
                result['reason'] = e
                return result
            time.sleep(1)
        
        result['success'] = True
        return result