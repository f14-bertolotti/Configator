
<img align="left" width="80px" src="https://raw.githubusercontent.com/f14-bertolotti/Configator/main/icon/icon-512px.png" />


# Configator

A very simple python3 library to manage json configuration from command line. 

### Basic Usage

Suppose that you have the following configuration file (`example.json`) for a script (`gen_images.py`):
```
{
    "size" : {
        "image_width"  : 100,
        "image_height" : 100
    },
    "no.images" : 14,
    "path" : "/some/path/"
}
```

In several occasion you may want to change some parts of the configuration to fit your needs.  
Instead of creating a new or modifying a default configuration each time,  
you can directly change some parts from the CLI.

For example, you can customize the configuration from CLI as:

```
python3 gen_images.py --configuration path/to/example.json 
                      --size.image_width 128
                      --path some/another/path
```

In `gen_images.py` you can access the configuration parameters by dot notation or indexing:


```
import configator

configuration = configator.Configator()

print(configuration.path)
print(configuration["size"]["image_width"])
```

You can also use multiple configuration files:

```
import configator

# this tells with which names the configurations will be addressed
configuration = configator.ConfigatorSwamp("cnf0","cnf1")

print(configuration.cnf0.path)
print(configuration.cnf1.size.image_width)
```

And you can customize the configuration from CLI as:
```
python3 gen_images.py --cnf0 path/to/example.json 
                      --cnf1 path/to/example2.json
                      --cnf0.size.image_width 128
                      --cnf1.path some/another/path
```


