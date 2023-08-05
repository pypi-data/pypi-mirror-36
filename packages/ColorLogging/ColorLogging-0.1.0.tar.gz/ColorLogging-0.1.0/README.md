# ColorLogging: A simple Python logger with colored log levels

[![GitHub version](https://badge.fury.io/gh/tjkessler%2FColorLogging.svg)](https://badge.fury.io/gh/tjkessler%2FColorLogging)
[![PyPI version](https://badge.fury.io/py/colorlogging.svg)](https://badge.fury.io/py/colorlogging)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/TJKessler/ColorLogging/master/LICENSE.txt)

## Installation:

### Prerequisites:
- Have Python 3.X installed
- Have the ability to install Python packages

### Method 1: pip
If your Python install contains pip:
```
pip install colorlogging
```
Note: if multiple Python releases are installed on your system (e.g. 2.7 and 3.6), you may need to execute the correct version of pip. For Python 3.X, change **pip install colorlogging** to **pip3 install colorlogging**.

### Method 2: From source
- Download the ColorLogging repository, navigate to the download location on the command line/terminal, and execute 
**"python setup.py install"**. 

## Usage

Import the ColorLogger with:
```python
from ColorLogging import ColorLogger
```

And initialize it:
```python
my_logger = ColorLogger()
```

You may change the directory that logs are saved to when initializing:
```python
my_logger = ColorLogger(log_dir='path/to/my/log/directory')
```

By default, the ColorLogger will log Debugging, Information, Warning, Error and Critical messages. To change the minimum level to log, specify it in the initialization of the ColorLogger or with set_level:
```python
my_logger = ColorLogger(set_level='info')
my_logger.set_level('warn')
```

To log a message, supply your desired log level and a message:
```python
my_logger.log('warn', 'This is a warning message!')
```

Supported log levels (in argument form) are:
- 'debug' (debugging)
- 'info' (information)
- 'warn' (warning)
- 'error' (error)
- 'crit' (critical)

## Contributing, Reporting Issues and Other Support:

To contribute to ColorLogging, make a pull request. Contributions should include tests for new features added, as well as extensive documentation.

To report problems with the software or feature requests, file an issue. When reporting problems, include information such as error messages, your OS/environment and Python version.

For additional support/questions, contact Travis Kessler (travis.j.kessler@gmail.com).