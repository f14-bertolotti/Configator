#!/usr/bin/env python3

from Configator.Configator import Configator 

import subprocess
import optparse
import unittest
import json
import os

class Test(unittest.TestCase):
    def test_configurable(self):
        working_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
        cnfpath = "tests/configurations/0.json"
        command = ["python3", "-m", "tests.scripts.simple", "--configuration", cnfpath, "--name3.name3.name0", "False"]
        cstmcnf = eval(subprocess.check_output(command, cwd=working_directory))
        self.assertEqual(cstmcnf["name3"]["name3"]["name0"], False)


