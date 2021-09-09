
from configator.Options import GatorOption as option
from configator.Fielder import Fielder     as fielder

import sys
import copy
import json    
import optparse
import functools


class GatorKey:
    def __init__(self, tokens=list()):
        self.tokens = tokens 
    def add(self, token):
        return GatorKey(self.tokens + [token])
    def __iter__(self):
        for token in self.tokens: yield token
    def __str__(self):
        return ".".join(self.tokens)
    def __repr__(self):
        return str(self)


class Configator:

    def __init__(self, path=None, base=None, name=None):

        ### REGISTER PARAMS #############################################################################
        self.__name__ = GatorKey([name] if name else [])
        self.__path__ = path if path or base else Configator.pop_configuration_path(sys.argv, str(self.__name__))

        ### THE ORIGINAL CONFIGURATION IS KEPT ###################################
        self.__base_configuration__   = fielder(Configator.load(self.__path__)) if not base else base
        self.__custom_configuration__ = copy.deepcopy(self.__base_configuration__)

        ### CREATE OPTIONS & PARSER FROM THE BASE CONFIGURATION ################################################
        self.__options__ = Configator.options(self.__base_configuration__, self.__name__)
        self.__parser__  = optparse.OptionParser(option_class=option, option_list=self.__options__[1])

        ### PARSE OPTIONS & UPDATE THE CONFIGURATION ####
        self.__parsed__ = self.__parser__.parse_args()[0]
        Configator.update(self.__custom_configuration__, self.__options__[0], self.__parsed__)   

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        return self.__custom_configuration__[key]

    @staticmethod
    def pop_configuration_path(arguments, name=None):
        name = name if name else "configuration"
        index = arguments.index(f"--{name}")
        arguments.pop(index)
        return arguments.pop(index)

    @staticmethod
    def update(configuration, keys, options):
        for key in keys:

            ### TRAVERSE THE CNF RECURSIVELY ################################
            temp_configuration = configuration
            for token in key.tokens[:-1]:
                temp_configuration = temp_configuration[token]

            ### UPDATE THE VALUE ############################################
            temp_configuration[key.tokens[-1]] = getattr(options, str(key))


    @staticmethod
    def options(configuration, prefix=GatorKey()):

        options, option_names = list(), list()
        ### CREAT OPTION WITH RECURSION IF THERE IS A NESTED DICT ###########################################################################################################
        for key, val in configuration.items():
            option_name = prefix.add(key)

            t_option_names, t_options = Configator.options(configuration[key], option_name) if type(val) == dict else \
                                        ([option_name], [option(f"--{str(option_name)}", action="store", type=type(val).__name__, dest=str(option_name), default=configuration[key])])

            option_names += t_option_names
            options      +=      t_options

        return option_names, options

    @staticmethod
    def load(path):
        with open(path, "r") as file: return json.loads(file.read())

    def __str__(self):
        return str(self.__custom_configuration__)

    def __repr__(self):
        return json.dumps(self.__custom_configuration__, indent=4, sort_keys=True)

