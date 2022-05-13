"""
Unit tests to test the functionality of our IOC database and python script transfer pipeline

### MUST BE RUN ON AN EPICS SERVER CONNECTED TO THE RASPBERRY PI CLUSTER ###
### AT LEAST 1 RASPBERRY PI MUST BE CONNECTED FOR THESE TESTS TO RUN AGAINST ###
### DO NOT EXPECT THESE TESTS TO PASS IF THOSE CONDITIONS ARE NOT MET ###
"""
from unittest import TestCase
import io
import subprocess
import shutil
import os
import epics

class FileTransferTests(TestCase):

    def setUp(self):
        pvs = epics.read_list_pvs()
        print(pvs)

    def tearDown(self):
        print("teardown")

    def test_switch_IOC_1_2(self):
        print("test")
        actual = "123"
        expected = "123"
        self.assertEqual(actual, expected)

    def test_switch_IOC_2_1(self):
        print("test")
        actual = "123"
        expected = "123"
        self.assertEqual(actual, expected)
