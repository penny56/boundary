'''
Created on Nov 19, 2021

@author: mayijie
'''

import zhmcclient
import time

class deleteHiperSocketAdapters():
    
    @classmethod
    def start(cls, dpmObj, hiperSocketSection):
        
        result = {'success': False, 'reason': ''}
        print ("\n")
        
        for hsAdapter in dpmObj.cpc.adapters.list(filter_args={'type':'hipersockets'}) :
            if hiperSocketSection["hiso_name_prefix"] in str(hsAdapter.name):
                try:
                    hsAdapter.delete()
                except (zhmcclient.HTTPError, zhmcclient.ParseError) as e:
                    result['reason'] = e
                    return result
                print ("HiperSocket: " + str(hsAdapter.name) + " deleted!")
            time.sleep(1)

        result['success'] = True
        return result