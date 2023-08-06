# sensorhandler
Multipurpose sensorhandler, read the value from source & do somethings (send, save, trigger, ...) with it, as configed.

## install

```bash:
pip install sensorhandler
```

## input
config.toml file on the current working directory. The contents of File is as follows:

```
[[sources]]
  name   = "dht22"
  errorhandler = "errorhandler"
  [[sources.values]]
    name = "temp"
    handlers = [
      "send"#import os, "save"
    ]
  [[sources.values]]
    name = "humidity"
    handlers = [
      "send"#, "save"
    ]
  [[sources.values]]
    name = "humiditydeficit"
    handlers = [
      "send"#, "save"
    ]


[[sources]]
  name   = "mh-z19"
  [[sources.values]]
    name = "co2"
    handlers = [
      "send", "save"
  ]
```

The array of table ***sources*** is the array of data source sensor definition, consist of followings:

- name: Sensor handler's name. The same name python file (with ".py" extention) will be dinamically imported and function ***read()*** on the imported module will be called. The return value of read() is expecte as a dictionally as key of value name and value like:
``` {'humiditydeficit': '15.9', 'temp': 26.8, 'humidity': 37.6}```

- values: handler difitition for each value, corresponding to the key of the dictionally of the return value of read() function.
  - name: value name
  
  - handlers: Value handler's name. The same name python file (with ".py" extention) will be dinamically imported and function ***handle(data_source_name, data_name, value):*** will be called with the Sensor handler's name, value name, and sensor value.
  
- errorhandler: Error handler's name. The same name python file (with ".py" extention) will be dinamically imported for error handling of Sensor value reading. Currently, just stab.

## How to use 
### as python program.

```bash:
python -m sensorhandler [--config config_file_path] [--imppath python_module_import_path] [ --list_imppath list_of_python_module_import_path]
```
In case no --config, "config.toml" on the running path is used.
The path specified by --imppath and --list_imppath is used ad additional Python import library path.

### as python library.

```python:
import sensorhandler

print (sensorhandler.read(config_file_path))
```

### history
- 0.1.1  2018.09.28  first version confirmed Raspberry Pi model B2+
- 0.1.2  2018.09.29  add config_file_path
- 0.1.3  2018.09.29  add --config, --imppath, --list_imppath
