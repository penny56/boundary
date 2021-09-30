'''
Created on Jan 15, 2019

@author: mayijie
'''

import zhmcclient
import time

class createPartition():
    
    @classmethod
    def start(cls, dpmObj, parSection):
        
        result = {'success': False, 'reason': ''}
        
        # if the partition already exist in the CPC
        try:
            parList = dpmObj.cpc.partitions.list()
        except Exception as e:
            result['reason'] = e
            return result
        
        for par in parList:
            if par.name == parSection["par_name"]:
                dpmObj.partition = par
                result['reason'] = "The partition already exist in the CPC, create failed."
                return result
        
        # construct partition template
        partitionTempl = dict()
        partitionTempl["name"] = parSection["par_name"]
        partitionTempl["type"] = parSection["par_type"]
        partitionTempl["description"] = parSection["par_desc"]
        partitionTempl["reserve-resources"] = True if (parSection["par_reserveresources"].lower() == 'true') else False
        partitionTempl["processor-mode"] = parSection["proc_mode"]
        partitionTempl["ifl-processors"] = int(parSection["proc_num"])
        if (int(parSection["init_mem"]) < 1024):
            partitionTempl["initial-memory"] = int(parSection["init_mem"]) * 1024
        else:
            partitionTempl["initial-memory"] = int(parSection["init_mem"])
        if (int(parSection["max_mem"]) < 1024):
            partitionTempl["maximum-memory"] = int(parSection["max_mem"]) * 1024
        else:
            partitionTempl["maximum-memory"] = int(parSection["max_mem"])

        try:
            new_partition = dpmObj.cpc.partitions.create(partitionTempl)
        except (zhmcclient.HTTPError, zhmcclient.ParseError) as e:
            result['reason'] = e
            return result
        time.sleep(1)
        
        try:
            parRet = dpmObj.cpc.partitions.find(name = partitionTempl["name"])
            dpmObj.partition = parRet
        except zhmcclient.NotFound as e:
            result['reason'] = e
            return result
        time.sleep(1)
        
        result['success'] = True
        return result

        