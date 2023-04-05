from configator.Options import GatorOption as Option
from configator.Fielder import Fielder     as Fielder
from configator.utils import yaml2dict, json2dict

import sys
import copy
import optparse
import dynamic_json
import dynamic_yaml


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
    """
    Configator manages a json configuration file as simple dictionary.
    It generate an option parser so that the configuration can be customized from command line.
    For example: given a configuration such as {A:1, B:2, C:{A:1}}, one can set C[A] = 2 from command line.
    The option available would be --A, --B, --C, --C.A
    One can also set the configuration itself from commandline using the option --configuration
    Also, the configuration can be customized dynamically with dot notation and indexing
    """

    def __init__(self, path=None, base=None, name=None):
        """
            Generate options for optparse.
            Parses options using optparse.
            Updates the configuration with the provided CLI args.

        Args:
            path: path to a json file representing the configuration.
            base: alternative to path, directly a dictionary representing the configuratio.
            name: sets the root name for all the options.

        """

        ### REGISTER PARAMS #############################################################################
        self.__name__ = GatorKey([name] if name else [])
        self.__path__ = path if path or base else Configator.pop_configuration_path(sys.argv, str(self.__name__))

        ### THE ORIGINAL CONFIGURATION IS KEPT ###################################
        self.__base_configuration__   = Fielder(Configator.load(self.__path__)) if not base else Fielder(base)
        self.__custom_configuration__ = copy.deepcopy(self.__base_configuration__)

        ### CREATE OPTIONS & PARSER FROM THE BASE CONFIGURATION ################################################
        self.__options__ = Configator.options(self.__base_configuration__, self.__name__)
        self.__parser__  = optparse.OptionParser(option_class=Option, option_list=self.__options__[1])

        ### PARSE OPTIONS & UPDATE THE CONFIGURATION ####
        self.__parsed__ = self.__parser__.parse_args()[0]
        Configator.update(self.__custom_configuration__, self.__options__[0], self.__parsed__)   

    def __getstate__(self):
        return {"__name__"                 : self.__name__,
                "__path__"                 : self.__path__,
                "__base_configuration__"   : self.__base_configuration__,
                "__custom_configuration__" : self.__custom_configuration__,
                "__options__"              : self.__options__,
                "__parser__"               : self.__parser__,
                "__parsed__"               : self.__parsed__}

    def __setstate__(self, dictionary):
        self.__name__                 = dictionary["__name__"] 
        self.__path__                 = dictionary["__path__"] 
        self.__base_configuration__   = dictionary["__base_configuration__"] 
        self.__custom_configuration__ = dictionary["__custom_configuration__"] 
        self.__options__              = dictionary["__options__"] 
        self.__parser__               = dictionary["__parser__"] 
        self.__parsed__               = dictionary["__parsed__"] 



    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        return self.__custom_configuration__[key]

    def __setitem__(self, key, val):
        self.__custom_configuration__[key] = val

    def __setattr__(self, key, val):
        if key.endswith("__") and key.startswith("__"): self.__dict__[key] = val
        else: self.__setitem__(key, val)


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
            if hasattr(options, str(key)) and getattr(options, str(key)) != None:
                temp_configuration[key.tokens[-1]] = getattr(options, str(key))
            



    @staticmethod
    def options(configuration, prefix=GatorKey()):

        options, option_names = list(), list()
        ### CREAT OPTION WITH RECURSION IF THERE IS A NESTED DICT ###########################################################################################################
        for key, val in configuration.items():
            option_name = prefix.add(key)

            if hasattr(val, "__getitem__") and hasattr(val, "__setitem__"):
                t_option_names, t_options = Configator.options(val, option_name)
            else:
                 t_option_names, t_options  = [option_name], [Option(f"--{str(option_name)}", action="store", type=type(val).__name__, dest=str(option_name))]

            option_names += t_option_names
            options      +=      t_options

        return option_names, options

    @staticmethod
    def load(path):
        if path.endswith(".json"):
            with open(path, "r") as file: return dynamic_json.load(file)
        if path.endswith(".yaml"):
            with open(path, "r") as file: return dynamic_yaml.load(file)       

    def __str__(self):
        if self.__path__ == None: return str(self.__custom_configuration__)
        if self.__path__.endswith(".json"): return str(json2dict(self.__custom_configuration__))
        if self.__path__.endswith(".yaml"): return str(yaml2dict(self.__custom_configuration__))

    def __repr__(self):
        return str(self)

