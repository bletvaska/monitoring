#!/usr/bin/env python3

import logging

class MyException(Exception):
    pass


print('>> before')

try:
    print('>> going to try block')
    raise MyException('this is wrong')
    with open('/etc/passwdxx', 'r') as f:
        print('hello world')

    value = 0
    result = 10 / value  # exception!!!
    print(result)

# except ZeroDivisionError as ex:
#     logging.error('you cannot divide by 0')
# 
# except PermissionError:
#     logging.error('You dont have permissions to access this file')
# 
# except FileNotFoundError:
#     logging.error('No such file or directory')
# 
except Exception as ex:
    logging.error('something went wrong')
    logging.exception(ex)

except Exception:
    # this will never happen
    pass


print('>> after')

