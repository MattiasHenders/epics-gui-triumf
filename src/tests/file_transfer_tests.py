"""
Unit tests to test the functionality of our IOC database and python script transfer pipeline

Tests can be run from Ubuntu using the command:
python3 -m unittest file_transfer_tests.py

### MUST BE RUN ON AN EPICS SERVER CONNECTED TO THE RASPBERRY PI CLUSTER ###
### THE EPICS SERVER NEEDS TO SERVE A softIoc WITH unittest.db, AND RUN server_startup.py ###
### ALWAYS START THE SERVER BEFORE STARTING THE RASPBERRY PI CLUSTER ###
### AT LEAST 1 RASPBERRY PI MUST BE CONNECTED FOR THESE TESTS TO RUN AGAINST ###
### RUNNING THESE TESTS WHILE OTHER USERS ARE RUNNING SCRIPTS ON THE RASPBERRY PIS MAY PRODUCE UNEXPECTED RESULTS ###
"""
from unittest import TestCase
from epics import PV, caget, cainfo
import io
import subprocess
import shutil
import os
import re
import shlex
import time

class FileTransferTests(TestCase):

    """
    Runs setup before any of the tests execute. Takes the first IOC found and gives it the UNIT_TEST_DB file to run
    tests with, stores its IP, original PV and kills its IOC.
    """
    @classmethod
    def setUpClass(cls):
        PVDict = {}
        cls.ProjectPath = os.path.expanduser('~') + "/epics-gui-triumf/src"
        with open(cls.ProjectPath + "/database/IOC/IOC_DEVICE_ASSOCIATIONS.txt") as file:
            for line in file:
                PVData = re.split('[=]', line.strip('\n'))
                PVDict[PVData[0]] = PVData[1]
        for key, value in PVDict.items():
            iocstatus = caget(key + ":status.INAV")
            if iocstatus is 1:
                cls.InitialPV = key
                pv = PV(key + ":device")
                cls.RPIAddress = pv.host[:-5]
                break
        cls.PVDict = PVDict
        subprocess.call(shlex.split(f"ssh-keygen -f '{os.path.expanduser('~') + '/.ssh/known_hosts'}' -R '{cls.RPIAddress}'"))
        subprocess.call(shlex.split(f"sshpass -p 'triumf' scp {cls.ProjectPath + '/database/IOC/UNIT_TEST_DB.db'}"
                                    f" pi@{cls.RPIAddress}:~"))
        subprocess.call(shlex.split(f"sshpass -p 'triumf' ssh pi@{cls.RPIAddress} \"pkill screen; screen -wipe; "
                                    f"sed -i 's/ID={FileTransferTests.InitialPV}/ID=testIoc1/' /home/pi/env/IOC_CONFIG\""))
        print("Using " + cls.InitialPV + " at " + cls.RPIAddress + " for testing..")

    """
    This method runs after all of the unit tests complete, and restores the RPI that was selected for testing back to its
    original state.
    """
    @classmethod
    def tearDownClass(cls):
        os.system(f"cp {cls.ProjectPath}/database/IOC/{cls.PVDict[cls.InitialPV]} {cls.ProjectPath}/database/dbconfig.db")
        os.system(f"cp {cls.ProjectPath}/scripts/IOC/{cls.PVDict[cls.InitialPV][:-2] + 'py'} {cls.ProjectPath}/scripts/run_script.py")
        os.system(f"sshpass -p 'triumf' scp {cls.ProjectPath + '/database/dbconfig.db'} pi@{cls.RPIAddress}:~")
        os.system(f"sshpass -p 'triumf' ssh -t pi@{cls.RPIAddress} "
                    f" \"pkill screen; screen -wipe; echo 'ID={cls.InitialPV}' > /home/pi/env/IOC_CONFIG "
                    f" && /usr/bin/screen -d -m sh -c '/opt/epics/epics-base/bin/linux-arm/softIoc "
                    f"-m IOC={cls.InitialPV} -d dbconfig.db && exec bash'\"")

    """
    This method runs before each unit test, restarting the IOC selected for testing.
    """
    def setUp(self):
        time.sleep(4)
        os.system(f"sshpass -p 'triumf' ssh -t pi@{FileTransferTests.RPIAddress} "
                  f"\"screen -d -m sh -c '/opt/epics/epics-base/bin/linux-arm/softIoc -m IOC=testIoc1 -d UNIT_TEST_DB.db'; exit\"")
        time.sleep(4)

    """
    This method runs after each unit test, killing any currently running screens on the selected RPI and setting its 
    IOC_CONFIG ID back to testIoc1.
    """
    def tearDown(self):
        os.system(f"sshpass -p 'triumf' ssh -t pi@{FileTransferTests.RPIAddress} "
                  f" \"echo 'ID=testIoc1' > /home/pi/env/IOC_CONFIG &&"
                                    f" pkill screen; screen -wipe\"")

    def test_PV_testing_IOC_connection(self):
        expected = 1
        time.sleep(8)
        actual = caget("testIoc1:status.INAV")
        self.assertEqual(actual, expected)

    def test_testing_PV_currently_disconnected(self):
        expected = 0
        actual = caget("testIoc2:status.INAV")
        self.assertEqual(actual, expected)

    def test_switch_to_test_PV(self):
        expected = 1
        subprocess.call(shlex.split(f"{FileTransferTests.ProjectPath}/scripts/server/assign_db.sh"
                                    f" testIoc1 testIoc2"))
        time.sleep(20)
        actual = caget("testIoc2:status.INAV")
        self.assertEqual(actual, expected)

    def test_original_ioc_disconnected_after_switch(self):
        expected = 0
        subprocess.call(shlex.split(f"{FileTransferTests.ProjectPath}/scripts/server/assign_db.sh"
                                    f" testIoc1 testIoc2"))
        time.sleep(20)
        actual = caget("testIoc1:status.INAV")
        self.assertEqual(actual, expected)

    def test_IOC_DESC(self):
        expected = "A test record"
        time.sleep(4)
        actual = caget("testIoc1.DESC")
        self.assertEqual(actual, expected)

    def test_switching_multiple_times(self):
        expected = 1
        subprocess.call(shlex.split(f"{FileTransferTests.ProjectPath}/scripts/server/assign_db.sh"
                                    f" testIoc1 testIoc2"))
        time.sleep(20)
        subprocess.call(shlex.split(f"{FileTransferTests.ProjectPath}/scripts/server/assign_db.sh"
                                    f" testIoc2 testIoc1"))
        time.sleep(20)
        actual = caget("testIoc1:status.INAV")
        self.assertEqual(actual, expected)
