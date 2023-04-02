import dynamic_yaml
import dynamic_json

def yaml2dict(yaml):
    return {k:yaml2dict(v) if isinstance(v,dynamic_yaml.yaml_wrappers.YamlDict) else v for k,v in yaml.items()}

def json2dict(json):
    return dict(json)
 
