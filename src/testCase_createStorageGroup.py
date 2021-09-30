'''
Created on Jul 15, 2020

@author: mayijie
'''

import zhmcclient
import time

class createStorageGroup():
    
    @classmethod
    def start(cls, dpmObj, createSgSection):
        
        result = {'success': False, 'reason': ''}
        
        sgDict = createSgSection
        sgTempl = dict()
        svTempl = dict()
        
        try:
            sgTempl['name'] = sgDict['sgname']
            sgTempl['cpc-uri'] = str(dpmObj.cpc.uri)
            if (sgDict.has_key('sgdesc') and sgDict['sgdesc'] != ''):
                sgTempl['description'] = sgDict['sgdesc']
            sgTempl['type'] = sgDict['stortype']
            # couldn't convert string to bool
            if (sgDict['sgshared'] == "True"):
                sgTempl['shared'] = True
            else:
                sgTempl['shared'] = False
            # max-partitions is the property for FCP only
            if (sgTempl['type'] == 'fcp'):
                sgTempl['max-partitions'] = int(sgDict['maxnumofpars'])
            sgTempl['connectivity'] = int(sgDict['numofpaths'])
            svsTempl = cls.constructSvTemplate(eval(sgDict['sgstorvolscfg']))
            sgTempl['storage-volumes'] = svsTempl
            sgTempl['email-to-addresses'] = ['noreply@ibm.com']
        except Exception as exc:
            print "[EXCEPTION constructSgTemplate]", exc
            raise exc
        
        try:
            dpmObj.console.storage_groups.create(sgTempl)
        except (zhmcclient.HTTPError, zhmcclient.AuthError, zhmcclient.ConnectionError, zhmcclient.ParseError) as e:
            result['reason'] = e
            return result

        time.sleep(1)
        
        # check the storage group exist in system
        try:
            for cpcSg in dpmObj.cpc.list_associated_storage_groups():
                if str(cpcSg.get_property('name')) == sgDict['sgname'] and str(cpcSg.get_property('fulfillment-state')) == 'pending':
                    result['success'] = True
                    return result
        except Exception as exc:
            print "[EXCEPTION list associated storage groups]", exc
            raise exc

        result['reason'] = "Could not find the storage group after creation."
        return result
    
    @classmethod
    def constructSvTemplate(cls, svCfgList):
        svsTempl = list()
        
        try:
            for sv in svCfgList:
                svTempl = dict()
                svTempl['operation'] = 'create'
                if (sv.has_key('storVolDesc') and sv['storVolDesc'] != ''):
                    svTempl['description'] = sv['storVolDesc']
                # for FICON, if model != EAV, the size property will not exist in the dict
                if (sv.has_key('storVolSize')):
                    svTempl['size'] = float(sv['storVolSize'])
                svTempl['usage'] = sv['storVolUse']
                
                # if the sg is for FICON, construct the FICON only properties
                if sv.has_key('storVolModel'):
                    svTempl['model'] = sv['storVolModel']
                
                if sv.has_key('storVolDevNum'):
                    svTempl['device-number'] = sv['storVolDevNum']
    
                svsTempl.append(svTempl)
        except Exception as exc:
            print "[EXCEPTION constructSvTemplate]", exc
            raise exc
        return svsTempl