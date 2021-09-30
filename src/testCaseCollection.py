'''
Created on Jan 15, 2019

How to add a new test case:

1. Create a new module and name it to testCase_newvNic.py
2. Add the import command in this module: from testCase_newvNic import newvNic
3. Add the method definition in this class: def test_newvNic(self):
4. Add the test_newvNic in the testcases section in the config file

@author: mayijie
'''

import unittest
import datetime
from dpm import dpm
from configFile import configFile
from testCase_createPartition import createPartition
from testCase_newvNic import newvNic
from testCase_attachFCP import attachFCP
from testCase_attachFICON import attachFICON
from testCase_newAccelerator import newAccelerator
from testCase_addCrypto import addCrypto
from testCase_setBootOption import setBootOption
from testCase_startPartition import startPartition
from testCase_dynamicChange import dynamicChange
from testCase_stopPartition import stopPartition
from testCase_detachStorageGroup import detachStorageGroup
from testCase_deletePartition import deletePartition
from testCase_createStorageGroup import createStorageGroup
from testCase_deleteStorageGroup import deleteStorageGroup


class testCaseCollection(unittest.TestCase):

    dpmObj = None

    @classmethod
    def setUpClass(cls):
        cls.config = configFile()
        cls.connSection = cls.config.sectionDict["connection"]
        cls.dpmObj = dpm(cls.connSection)
        
        print '||| HMC: ' + cls.connSection['hmc'] + ' SE: ' + cls.connSection['cpc'] + ' auto regression test verified at ' + str(datetime.datetime.now()).split('.')[0] + ' >>>'


    @classmethod
    def tearDownClass(cls):
        #destructHMCConnection()
        pass
    
    
    def test_createPartition(self):
        # Start test case: create partition ...
        result = createPartition.start(self.dpmObj, self.config.sectionDict["partition"])
        self.assertTrue(result['success'], result['reason'])

        
    def test_newvNic(self):
        # Start test case: add vNic ...
        result = newvNic.start(self.dpmObj, self.config.sectionDict["vnic"])
        self.assertTrue(result['success'], result['reason'])
    
    def test_attachFCP(self):
        # Start test case: attach FCP storage group...
        result = attachFCP.start(self.dpmObj, self.config.sectionDict["attachfcp"])
        self.assertTrue(result['success'], result['reason'])

    def test_attachFICON(self):
        # Start test case: attach FICON storage group...
        result = attachFICON.start(self.dpmObj, self.config.sectionDict["attachficon"])
        self.assertTrue(result['success'], result['reason'])
        
    def test_newAccelerator(self):
        # Start test case: new accelerator virtual function...
        result = newAccelerator.start(self.dpmObj, self.config.sectionDict["accelerator"])
        self.assertTrue(result['success'], result['reason'])

    def test_addCrypto(self):
        # Start test case: add crypto ...
        result = addCrypto.start(self.dpmObj, self.config.sectionDict["crypto"])
        self.assertTrue(result['success'], result['reason'])

    def test_setBootOption(self):
        # Start test case: set boot option ...
        result = setBootOption.start(self.dpmObj, self.config.sectionDict["boot"])
        self.assertTrue(result['success'], result['reason'])
        
    def test_startPartition(self):
        # Start test case: start the partition ...
        result = startPartition.start(self.dpmObj)
        self.assertTrue(result['success'], result['reason'])
        
    def test_dynamicChange(self):
        # Start test case: dynamic update the partition resource ...
        result = dynamicChange.start(self.dpmObj, self.config.sectionDict["dynamic"], self.config.sectionDict["connection"])
        self.assertTrue(result['success'], result['reason'])

    def test_stopPartition(self):
        # Start test case: stop the partition ...
        result = stopPartition.start(self.dpmObj)
        self.assertTrue(result['success'], result['reason'])

    def test_detachStorageGroup(self):
        # Start test case: detach storage groups from a partition ...
        result = detachStorageGroup.start(self.dpmObj)
        self.assertTrue(result['success'], result['reason'])

    def test_deletePartition(self):
        # Start test case: delete the partition ...
        result = deletePartition.start(self.dpmObj)
        self.assertTrue(result['success'], result['reason'])

    def test_createFcpStorageGroup(self):
        # Start test case: create FCP storage group ...
        result = createStorageGroup.start(self.dpmObj, self.config.sectionDict["createfcp"])
        self.assertTrue(result['success'], result['reason'])

    def test_deleteFcpStorageGroup(self):
        # Start test case: delete FCP storage group ...
        result = deleteStorageGroup.start(self.dpmObj, self.config.sectionDict["createfcp"])
        self.assertTrue(result['success'], result['reason'])
    
    def test_createFiconStorageGroup(self):
        # Start test case: create FICON storage group ...
        result = createStorageGroup.start(self.dpmObj, self.config.sectionDict["createficon"])
        self.assertTrue(result['success'], result['reason'])

    def test_deleteFiconStorageGroup(self):
        # Start test case: delete FICON storage group ...
        result = deleteStorageGroup.start(self.dpmObj, self.config.sectionDict["createficon"])
        self.assertTrue(result['success'], result['reason'])
    