#!/usr/bin/env python3
import unittest, copy
from configator.Fielder import Fielder 

dictionary = {"A":"B","C":{"A":"B","C":{"A":"B"}}}
fielder    = Fielder(dictionary)

class Test(unittest.TestCase):

    def test_getattr(self):
        self.assertEqual(fielder.A, dictionary["A"])
        self.assertEqual(fielder.C.A, dictionary["C"]["A"])
        self.assertEqual(fielder.C.C.A, dictionary["C"]["C"]["A"])

    def test_getitem(self):
        self.assertEqual(fielder["A"], dictionary["A"])
        self.assertEqual(fielder["C"]["A"], dictionary["C"]["A"])
        self.assertEqual(fielder["C"]["C"]["A"], dictionary["C"]["C"]["A"])

    def test_setattr(self):
        fielder.A = "D"
        fielder.C.A = "E"
        fielder.C.C.A = "T"
        self.test_getitem()
        self.test_getattr()

    def test_setitem(self):
        fielder["A"] = "K"
        fielder["C"]["A"] = "J"
        fielder["C"]["C"]["A"] = "L"
        self.test_getitem()
        self.test_getattr()

    def test_dictionary(self):
        self.assertEqual(fielder.__dictionary__, dictionary)

    def test_deepcopy(self):
        fieldercopy = copy.deepcopy(fielder)
        self.assertTrue(not (fieldercopy is fielder))
        self.assertTrue(fieldercopy.__dictionary__ == fielder.__dictionary__)
