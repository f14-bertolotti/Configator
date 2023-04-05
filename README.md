
<img align="left" width="80px" src="https://raw.githubusercontent.com/f14-bertolotti/Configator/main/icon/icon-512px.png" />


# Configator

A very simple python3 library to manage dynamic json/yaml (see [dynamic-yaml]) configuration from command line. 

### Basic Usage

Suppose that you have the following configuration file (`example.json`) for a script (`gen_images.py`):
```
{
    "root" : "home",
    "size" : {
        "image_width"  : 100,
        "image_height" : 100
    },
    "no.images" : 14,
    "path" : "{root}/some/path/"
}
```

In several occasion you may want to change some parts of the configuration to fit your needs.  
Instead of creating a new or modifying a default configuration each time,  
you can directly change some parts from the CLI.

For example, you can customize the configuration from CLI as:

```
python3 gen_images.py --configuration path/to/example.json 
                      --size.image_width 128
                      --root "/home/usr"
```

In `gen_images.py` you can access and modify the configuration parameters by dot notation or indexing:


```
import configator

configuration = configator.Configator()

print(configuration.path)
configuration.path = "~/data"
print(configuration["size"]["image_width"])
```

Also notice that updating ```root``` affects the parameter ```path```.

[dynamic-yaml]: <https://github.com/childsish/dynamic-yaml>
