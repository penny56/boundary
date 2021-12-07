'''
Created on Nov 16, 2020

@author: mayijie
'''

import unittest
import sys
from testCaseCollection import testCaseCollection
from configFile import configFile

class boundary:
    
    def __init__(self, testCaseList, configFileName):
        self.suite = unittest.TestSuite()
        self.tests = []
        
        # the sequence is matter, it's the order the cases execute
        for testCase in testCaseList:
            self.tests.append(testCaseCollection(testCase))
        
        self.suite.addTests(self.tests)

    def start(self):
        #unittest.main(self.suite)
        self.runner = unittest.TextTestRunner(verbosity=3)
        self.result = self.runner.run(self.suite)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        location = sys.argv[1]
    else:
        print ("Please input the config file location as a parameter!\nQuitting....")
        exit(1)
    
    # pass the config file
    config = configFile(location)
    config.loadConfig()
    testCaseList = eval(config.sectionDict['testplans']['1120'])
    configFileName = location.split('/')[-1].split('.')[0]
    
    # create a boundary object
    boundary = boundary(testCaseList, configFileName)
    boundary.start()