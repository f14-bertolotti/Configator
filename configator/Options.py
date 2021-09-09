import optparse
import copy

str2bool = {"True":True,"False":False}
def check(option, opt, val):
    try: return str2bool[val]
    except KeyError: 
        raise optparse.OptionValueError(f"option {opt}: invalid bool value {val}.")


class GatorOption(optparse.Option):
    TYPES = optparse.Option.TYPES + ("bool",) 
    TYPE_CHECKER = copy.copy(optparse.Option.TYPE_CHECKER)
    TYPE_CHECKER["bool"] = check


