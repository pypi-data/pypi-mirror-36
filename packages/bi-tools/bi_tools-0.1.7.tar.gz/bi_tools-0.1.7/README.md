# bi_tools

# Introduction
bi_tools

- BI Logger
- BI Parser
- Flex Read
- Flex Write

## Installation

To install, clone this repository and run ez_bi_tools_installer.sh by running

```
sh /home/$USER/bitools/BILogger/ez_bi_tools_installer.sh
```

## Log Level

LEVELS:

CRITICAL	50

ERROR	    40

WARNING	  30

INFO	    20

DEBUG	    10

NOTSET     0

## Date format
'2018-06-08'

## Parser Example Usage
```python
from bi_tools import Parser
Parser = Parser()
Parser.exc_date
#returns execution date
Parser.mode
#returns log level
```

## Logger Example Usage

```python
from bi_tools import Logger

Logger = Logger(mode="debug")

Logger.custom_log("custom log")
#prints 'custom log' in your log file

Logger.execution_date()
#prints 'Execution Date: {EXECUTION_DATE}' in your log file

Logger.exist()
#prints 'data exists' in your log file

Logger.not_exist()
#prints 'data does not exist' in your log file

Logger.writing()
#prints 'writing table...' in your log file

Logger.querying()
#prints 'querying...' in your log file

Logger.success()
#prints 'succeeded' in your log file

Logger.fail()
#prints 'failed' in your log file

Logger.ran_info
#prints 'ran by {USER} & ran on {DATETIME}' in your log file
```
## Logger & Parser Usage Together

```python
def main(date):
    print date
    logger.custom_log("successfully printed date")

if __name__ == "__main__":
    args = Parser() #parse arguments
    logger = Logger(mode="debug", exc_date=args.exc_date) #use the parsed arguments to set the logger
    main(args.exc_date) #use the parsed argument to run the main body of code
```

## Flex Read Usage
```python
from bi_tools import flex_read
df = flex_read("C:/Users/user_name/example.csv")
# loads csv locally

df = flex_read("C:/Users/user_name/example.h5")
# loads hdf5 locally

df = flex_read("s3://s3-bucket/example.csv", s3=True)
# loads csv from s3
```

## Flex Write Usage
```python
from bi_tools import flex_write
flex_write(df, "C:/Users/user_name/example.csv")
# wrties csv locally

flex_write(df, "C:/Users/user_name/example.h5")
# writes hdf5 locally

flex_read(df, "s3://s3-bucket/example.csv", s3=True)
# writes csv to s3
```
