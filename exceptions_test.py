import logging

print('Start')

try:
    print('entering danger zone')
    file = open('this.one.is.not.available', 'r')
    10 / 0
    print('leaving danger zone')
except ZeroDivisionError as ex:
    logging.error('Error: we have zero division error')
    logging.exception(ex)
except PermissionError as ex:
    logging.error('Error: Wrong permissions')
    logging.exception(ex)
except Exception as ex:
    logging.error('Error: something strange happened')
    logging.exception(ex)
    
print('End')
