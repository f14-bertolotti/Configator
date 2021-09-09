#!/usr/bin/env python3

from configator.ConfigatorSwamp import ConfigatorSwamp

import subprocess
import optparse
import unittest
import json
import os

class Test(unittest.TestCase):
    def test_configurable(self):
        working_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
        
        script   = "tests.scripts.swamp"
        cnfpath0 = "tests/configurations/0.json"
        cnfpath1 = "tests/configurations/1.json"
        cnfname0 = "--cnf0"
        cnfname1 = "--cnf1"

        command = ["python3", "-m", script, cnfname0, cnfpath0, cnfname1, cnfpath1, f"{cnfname1}.name3.name3.name0", "False"]
        cstmcnf = eval(subprocess.check_output(command, cwd=working_directory))

        self.assertEqual(cstmcnf[cnfname1[2:]]["name3"]["name3"]["name0"], False)


