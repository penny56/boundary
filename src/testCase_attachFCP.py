'''
Created on Jan 21, 2019

[fcp]
vhba_list = ['M90_WEI_Boot_Dedicated_SG:8100', 'M90_WEI_Boot_Dedicated_SG:8000', 'M90_LNXT01_XIV_Dedicated_SG:9000', 'M90_LNXT01_XIV_Dedicated_SG:9100']

@author: mayijie
'''

import zhmcclient
import time

class attachFCP():

    @classmethod
    def start(cls, dpmObj, fcpSection):
        
        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        sgDevNumDict = dict()
        cpcActiveFCPSgDict = dict()
        
        # Parse the fcpSection
        vhbaList = eval(fcpSection['vhba_list'])
        for vhba in vhbaList:
            # e.g. vhba = 'M90_KVMT02_XIV_Dedicated_SG:9000'
            vhbaProp = vhba.split(':')
            if vhbaProp[0] in sgDevNumDict:
                sgDevNumDict[vhbaProp[0]].append(vhbaProp[1])
            else:
                sgDevNumDict[vhbaProp[0]] = [vhbaProp[1]]
        
        # Attach the storage group(s) and set the correct device number(s)
        try:
            cpcSgs = dpmObj.cpc.list_associated_storage_groups()
        except zhmcclient.HTTPError as e:
            result['reason'] = e
            return result

        for cpcSg in cpcSgs:
            if cpcSg.get_property('type') == 'fcp' and cpcSg.get_property('fulfillment-state') == 'complete':
                cpcActiveFCPSgDict[cpcSg.name] = cpcSg
        
        for sgName, sgDevNumList in sgDevNumDict.items():
            # Check if the sgName exist in the cpc, the type is FCP and the state is complete
            if sgName in cpcActiveFCPSgDict.keys():
                try:
                    dpmObj.partition.attach_storage_group(cpcActiveFCPSgDict[sgName])
                except zhmcclient.HTTPError as e:
                    result['reason'] = e
                    return result
                
                # set the device number(s)
                try:
                    vsrs = cpcActiveFCPSgDict[sgName].virtual_storage_resources.list()
                except zhmcclient.HTTPError as e:
                    result['reason'] = e
                    return result
                
                if len(sgDevNumList) == len(vsrs):
                    # the number of devnum in the config file match the path number of the storage group
                    for vsr in vsrs:
                        newValue = dict()
                        adapterDesc = cls.getAdapterDesc(dpmObj, vsr.get_property('adapter-port-uri'))

                        if "Cisco" in adapterDesc.split(' '):
                            # for cisco, they use the smaller device number, make the smallest to the last
                            sgDevNumList.sort(reverse=True)
                        elif "Brocade" in adapterDesc.split(' '):
                            # for brocade vhba, they use the bigger device number, put the biggest to the last
                            sgDevNumList.sort()

                        newValue['device-number'] = sgDevNumList.pop()
                        try:
                            vsr.update_properties(newValue)
                        except zhmcclient.HTTPError as e:
                            result['reason'] = e
                            return result
                else:
                    result['reason'] = "The number of device number: %s in config file not sync with the storage group path number: %s!" % (len(sgDevNumList), len(vsrs))
                    return result
                
                time.sleep(1)
                
                # check if the attach action completed successfully
                try:
                    if len(cpcActiveFCPSgDict[sgName].list_attached_partitions(name = dpmObj.partition.get_property("name"))) != 1:
                        result['reason'] = "The storage group %s attached failed while checking after the attachment action!" % (sgName)
                        return result
                except zhmcclient.HTTPError as e:
                    result['reason'] = e
                    return result
            else:
                result['reason'] = "The storage group %s is not exist or not in complete state!" % (sgName)
                return result
        time.sleep(1)
        
        result['success'] = True
        return result
    
    @classmethod
    def getAdapterID(cls, dpmObj, adapterPortUri):
        adapterUri = adapterPortUri.split('/storage-ports/')[0]
        filter_args = {'object-uri': adapterUri}
        adapterObj = dpmObj.cpc.adapters.find(**filter_args)
        adapterID = adapterObj.name.split(' ')[1]
        return adapterID

    @classmethod
    def getAdapterDesc(cls, dpmObj, adapterPortUri):
        adapterUri = adapterPortUri.split('/storage-ports/')[0]
        filter_args = {'object-uri': adapterUri}
        adapterObjs = dpmObj.cpc.adapters.list(full_properties=True, filter_args=filter_args)
        return adapterObjs[0].get_property("description")
 