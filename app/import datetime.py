import datetime


def string_to_datetime(string):
    return datetime.datetime.strptime(string, '%M:%S')


possible = string_to_datetime('10:00') - string_to_datetime('00:48')
ee = '8:59'
eepb = '9:00'
if string_to_datetime(ee) < string_to_datetime(eepb) and string_to_datetime(ee) - string_to_datetime('00:00') < string_to_datetime('10:00') - string_to_datetime('00:48'):
    print('eepb')

print(possible)
print(ee)
print(eepb)