import Configator.Options as options
import optparse           as  parser

import json     
import functools

def p(x):print("=", x,"=");return x

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

    def __init__(self, path="./configuration.json"):
        self.conf = Configator.load(path)
        self.path = path
        self.keys,self.opts = Configator.options(self.conf)
        self.prsr = parser.OptionParser(option_class=options.GatorOption,
                                        option_list =self.opts)
        self.vals = self.prsr.parse_args()[0]
       
        for key in self.keys:
            tmp = self.conf
            for tkn in key.tokens[:-1]:
                tmp = tmp[tkn]
            tmp[key.tokens[-1]] = getattr(self.vals, str(key))

            

        
    @staticmethod
    def apply(key,val,cnf):
        print()
        tkns = key.split(".")
        cnf = functools.reduce(lambda x,y: p(x[y]),[cnf] + tkns.tokens[:-1])
        cnf[tkns.tokens[-1]] = val
    
    @staticmethod
    def options(conf, prefix=GatorKey()):

        opts, keys = list(), list()
        for key, val in conf.items():
            token = prefix.add(key)

            if type(val) == dict:
                optname_tmp, options_tmp = Configator.options(conf[key], token)
                keys += optname_tmp
                opts += options_tmp                 
            else:
                keys.append(token)
                opts.append(options.GatorOption(f"--{str(prefix.add(key))}", 
                                                action="store", 
                                                type=type(val).__name__, 
                                                dest=str(token), 
                                                default=conf[key]))
       
        return keys, opts                

    @staticmethod
    def load(path):
        with open(path, "r") as file:
            conf = json.loads(file.read())
        return conf

    def __str__(self):
        return str(self.conf)

    def __repr__(self):
        return json.dumps(self.conf, indent=4, sort_keys=True)

