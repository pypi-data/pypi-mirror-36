Simple python configuration tool
================================
ezcfg is a python package that allow you to easily maintain and access 
configuration throughout your project 

* easy registration of configuration
* easy access to configuration
* easy type validation of configuration
* easy loading of configuration from json, ini, or environment variables

How to install
--------------
```bash
pip install ezcfg
```

How to use
----------
register your first configuration
```python
from ezcfg.config import ezcfg
ezcfg.register_config(name='myfirstconfig', config_type=str, default='configvalue')

# Access of configuration
print(ezcfg.myfirstconfig)
# "configvalue"
```
load your config from ini, json, and environment variables
```python
from ezcfg.config import ezcfg
ezcfg.register_config(name='myfirstconfig', config_type=str, default='configvalue')
# load config from json file
ezcfg.load_config_from_json_file('myconfigpath.json')

# load config from ini file
ezcfg.load_config_from_ini_file('myconfigpath.ini', section='DEFAULT')

# load config from environment variables
# you first need to set env_var name
ezcfg.register_config(name='myfirstconfig', config_type=str, default='configvalue', env_var='MYFIRSTCONFIG')
# this will load from MYFIRSTCONFIG env var
ezcfg.load_config_from_env()
```
automatic type checking
```python
from ezcfg.config import ezcfg
# will raise TypeError
ezcfg.register_config(name='myfirstconfig', config_type=int, default='configvalue')
```

status
------
[![Build Status](https://travis-ci.com/shalev67/EZconfig.svg?branch=master)](https://travis-ci.com/shalev67/EZconfig)
