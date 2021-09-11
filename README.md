
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

For example, you can access the configuration as:

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


