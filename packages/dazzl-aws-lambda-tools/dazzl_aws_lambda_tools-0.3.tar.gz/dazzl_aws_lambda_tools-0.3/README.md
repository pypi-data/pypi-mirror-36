# LIB Dazzl Lambda Tools | [![Build Status](https://travis-ci.org/dazzl-tv/dazzl-aws-lambda-tools.svg?branch=master)](https://travis-ci.org/dazzl-tv/dazzl-aws-lambda-tools) [![Requirements Status](https://requires.io/github/dazzl-tv/dazzl-aws-lambda-tools/requirements.svg?branch=master)](https://requires.io/github/dazzl-tv/dazzl-aws-lambda-tools/requirements/?branch=master)

Library python for simplify to create lambda function (AWS lambda) and Dazzl API service.

The authentication is automatically executed and use a environment variable.

## How to use

```python
# Import
import dazzl_aws_lambda_tools as aws_lambda

# Initialize
# It's a bucket event
dz = aws_lambda.Tools(record)

# Send a request to backend
path = '/super/path/with/id/and/another/data'
body = { 'foo' 'bar' }
dz.send('POST', path, body)

# Get name to bucket
dz.bucket_name()

# Get key to bucket
dz.bucket_key()
```

## Logger and environments

The logger has different level :
-  development has level `DEBUG`,
- staging has level `INFO`,
- production has level `ERROR`

__if you want customize log level use variable environment `LOG_LEVEL`__

For more information see : [Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels)

## Variables environments

| Name             | Value example    | Required                        |
| --               | --               | --                              |
| `LOG_LEVEL`      | info             | `false`                         |
| `URL_API__<env>` | https://dazzl.tv | `true` if you want send request |
| `USERNAME_<env>` | roger@dazzl.tv   | `true` if you want send request |
| `PASSWORD_<env>` | hidden_password  | `true` if you want send request |

`<env>` is a environment type :
- development : `DEVE`
- staging :  `STAG`
- production : `PROD`

## Convention bucket name

The bucket name exist for three environment :

| Environment | Example bucket name     |
| --          | --                      |
| development | suffix.name.development |
| staging     | suffix.name.staging     |
| production  | suffix.name             |

## Script test

```linux
clear; python3 -m memory_profiler ./tests/requests.py ; python3 -m memory_profiler ./tests/simple.py
```
