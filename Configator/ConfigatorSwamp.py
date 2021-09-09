
from Configator.Configator import Configator

import json, copy, sys

class ConfigatorSwamp:
    def __init__(self, *args):
       
        self.__names__ = args
        self.__argvs__ = copy.deepcopy(sys.argv)
        self.__paths__ = ConfigatorSwamp.pop_path_argvs(self.__names__, self.__argvs__)

        sys.argv = self.__argvs__
        self.__super_configuration__ = Configator(base={name:Configator.load(path) for name,path in zip(self.__names__, self.__paths__)})

    def __getattr__(self, key):
        return self[key]

    def __getitem__(self, key):
        return self.__super_configuration__[key]

    def __str__(self):
        return str(self.__super_configuration__)

    def __repr__(self):
        return repr(self.__super_configuration__)

    @staticmethod
    def pop_path_argvs(names, argvs):
        paths = list()
        for nameidx in range(len(names)):
            argvidx = argvs.index(f"--{names[nameidx]}")
            argvs.pop(argvidx)
            paths.append(argvs.pop(argvidx))
        return paths
