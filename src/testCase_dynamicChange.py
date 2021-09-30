'''
Created on Feb 25, 2019

Mar. 21 20119 - add the status check in the very beginning

@author: mayijie
'''

import zhmcclient
import time, threading

class dynamicChange():
    
    retCmdline = None
    
    @classmethod
    def start(cls, dpmObj, dynamicSection, conSection):

        result = {'success': False, 'reason': ''}
        if dpmObj.partition == None:
            result['reason'] = "Please guarantee the partition created success in the 1st test case!"
            return result
        
        processorDelta = int(dynamicSection['processor'])
        memoryDelta = int(dynamicSection['memory'])

        # check up the status
        try:
            dpmObj.partition.wait_for_status(status="active", status_timeout=5)
        except zhmcclient.StatusTimeout as e:
            result['reason'] = "The partition should be in active state before this test case."
            return result

        # Logon the system
        time.sleep(60)
        topic = dpmObj.partition.open_os_message_channel(include_refresh_messages=False)
        receiver = zhmcclient.NotificationReceiver(topic, conSection["hmc"], conSection["uid"], conSection["psw"])
        
        dpmObj.partition.send_os_command('\n')
        time.sleep(5)
        dpmObj.partition.send_os_command('\n')
        time.sleep(5)
        
        dpmObj.partition.send_os_command(conSection["par_uid"])
        time.sleep(5)
        dpmObj.partition.send_os_command(conSection["par_psw"])
        time.sleep(5)
        if cls.listenOSM(receiver, "Last login", 10) == None:
            result['reason'] = "Login failed!"
            return result
            
        # update the partition to increase the processor number
        oldProcessor = dpmObj.partition.get_property('ifl-processors')

        partitionTempl = dict()
        partitionTempl["ifl-processors"] = oldProcessor + processorDelta
        
        try:
            dpmObj.partition.update_properties(partitionTempl)
        except (zhmcclient.HTTPError, zhmcclient.ParseError) as e:
            result['reason'] = e
            return result
        time.sleep(5)
        
        # verify the partition parameters updated
        if dpmObj.partition.get_property('ifl-processors') != partitionTempl["ifl-processors"]:
            result['reason'] = "Processor value updated failed."
            return result

        # verify the processor number by Linux command
        dpmObj.partition.send_os_command('lscpu')
        currProcLine = cls.listenOSM(receiver, "CPU(s)", 30)
        if currProcLine == None:
            result['reason'] = "Couldn't get the current processor command line from OSM."
            return result
        currProcNumber = int(currProcLine.split(':')[-1].strip())
        if currProcNumber != partitionTempl["ifl-processors"] * 2:
            result['reason'] = "Processor value updated failed by lscpu command."
            return result
        
        # do the same thing for memory
        '''
        oldMemory = dpmObj.partition.get_property('initial-memory')
        partitionTempl.clear()
        partitionTempl["initial-memory"] = oldMemory + (memoryDelta * 1024)
        try:
            dpmObj.partition.update_properties(partitionTempl)
        except (zhmcclient.HTTPError, zhmcclient.ParseError) as e:
            result['reason'] = e
            return result
        time.sleep(5)
        
        if dpmObj.partition.get_property('initial-memory') != partitionTempl["initial-memory"]:
            result['reason'] = "Memory value updated failed."
            return result

        dpmObj.partition.send_os_command("chmem -e " + str(memoryDelta) + "G")
        time.sleep(5)
        dpmObj.partition.send_os_command('lsmem')
        time.sleep(5)
        currMemLine = cls.listenOSM(receiver, "Total online memory", 30)
        if currMemLine == None:
            result['reason'] = "Couldn't get the total online memory command line from OSM."
            return result
        currMemNumber = int(currMemLine.split(':')[-1].strip().split(' ')[0])
        if currMemNumber != partitionTempl["initial-memory"]:
            result['reason'] = "Processor value updated failed by lsmem command."
            return result
        '''    

        
        # I don't know but it will hang a long time if I close the channel
        # receiver.close()
        
        result['success'] = True
        return result
    
    @classmethod
    def parseOSM(cls, receiver, target_txt):
        global retCmdline
        try:
            for headers, message in receiver.notifications():
                os_msg_list = message['os-messages']
                for os_msg in os_msg_list:
                    msg_box = os_msg['message-text'].strip('\n')
                    for msg_line in msg_box.split('\n'):
                        if msg_line.find(target_txt) != -1:
                            retCmdline = msg_line
                            return
        except KeyboardInterrupt:
            return None
    
    @classmethod
    def listenOSM(cls, receiver, target_txt, expireSec):
        global retCmdline
        t = threading.Thread(target=cls.parseOSM, args=(receiver, target_txt))
        t.start()
        t.join(expireSec)
        if t.isAlive():
            # timer expired, terminate the thread
            pass
        elif retCmdline != None:
            return retCmdline
        else:
            # Error, the parseOSM return before timer expired, but return with None
            pass
        return None