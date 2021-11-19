'''
Created on Nov 09, 2021

@author: mayijie
'''

import zhmcclient
import time

class createHiperSocketAdapters():
    
    @classmethod
    def start(cls, dpmObj, hiperSocketSection):
        
        result = {'success': False, 'reason': ''}

        NUM = int(hiperSocketSection['cnt'])
        hsTempl = dict()
        print '\n'
        
        while NUM != 0:
            
            hsTempl['name'] = hiperSocketSection['hiso_name_prefix'] + str(NUM)
            
            try:
                new_adapter = dpmObj.cpc.adapters.create_hipersocket(hsTempl)
                print "HiperSocket: " + hsTempl['name'] + " created!"
            except (zhmcclient.HTTPError, zhmcclient.ParseError) as e:
                result['reason'] = e
                return result
            
            time.sleep(1)
            hsTempl.clear()
            NUM -= 1
        
        result['success'] = True
        return result