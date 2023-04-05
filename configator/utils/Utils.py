import dynamic_yaml
import dynamic_json

def yaml2dict(yaml):
    return {k:yaml2dict(v) if isinstance(v,dynamic_yaml.yaml_wrappers.YamlDict) else yaml[k] for k,v in yaml.items()}

def json2dict(json):
    return {k:json2dict(v) if isinstance(v,dynamic_json.json_wrappers.JsonDict) else json[k] for k,v in json.items()}
 
