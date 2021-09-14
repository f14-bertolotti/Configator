#!/usr/bin/env python3

from configator.Configator import Configator 

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

    def test_assignement(self):
        cnf = Configator("tests/configurations/0.json")
        cnf.name3 = False
        cnf["name2"] = 10 
        self.assertEqual(cnf.__custom_configuration__.__dictionary__["name3"], False)
        self.assertEqual(cnf.__custom_configuration__.__dictionary__["name2"], 10)

    def test_from_dict(self):
        cnf = Configator(base={"a":1,"b":2,"c":{"d":1}})
        cnf.c.d = 10
        self.assertEqual(cnf.__custom_configuration__.__dictionary__["c"]["d"], 10)
