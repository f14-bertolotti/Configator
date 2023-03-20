import copy
import json

class Fielder:
    """

    Fielder wraps a dictionary which can be accessed using also the dot notation.
    For example: 
        Given: d = {A: 1, B: 2, C:{A:1}}
        The following operation are permitted:
            d.A
            d.A.C
            d["A"]
            d.A.C = 2
            d["A"]["C"] = 2

    Attributes:
        __dictionary__ : the wrapped dictionary.

    """
    def __init__(self, dictionary):
        self.__dictionary__ = dictionary

    def __getattr__(self, key):
        try: return getattr(self.__dictionary__, key)
        except AttributeError:
            return Fielder(self.__dictionary__[key]) if type(self.__dictionary__[key]) == dict else self.__dictionary__[key]

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        self.__dictionary__[key] = val 

    def __getstate__(self):
        return self.__dictionary__

    def __setstate__(self, state):
        self.__dictionary__ = state

    def __setattr__(self, key, val):
        if key == "__dictionary__": self.__dict__[key] = val
        else: self.__setitem__(key, val)

    def __deepcopy__(self, memo):
        result = self.__class__.__new__(self.__class__)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    def __str__(self):
        return str(self.__dictionary__)

    def __repr__(self):
        return json.dumps(str(self.__dictionary__))



