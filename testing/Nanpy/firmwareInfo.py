#!/usr/bin/python3
import time, nanpy
import nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

#### From nanpy's test code ####
#Doesn't work for me. Possible firmware configuration missing
try:
	print('Nanpy test code firmware info:')
	print('Firmware classes enabled in cfg.h:')
	print('  ' + '\n  '.join(at.connection.classinfo.firmware_name_list))

	d = at.define.as_dict
	print(
		'\nYour firmware was built on:\n  %s %s' %
		(d.get('__DATE__'), d.get('__TIME__')))
except Exception as e:
	print('Nanpy test code firmware info Exception')
	print(e)

#### My firmware info code ####
print('My firmware info:')

print('\nat.firmware_info')
try:
	firmwareInfoDict = at.firmware_info
	print('avr_name            ' + firmwareInfoDict['avr_name'])
	print('arduino_version     ' + firmwareInfoDict['arduino_version'])
	print('compile_datetime    ' + str(firmwareInfoDict['compile_datetime']))
	print('gcc_version         ' + firmwareInfoDict['gcc_version'])
	print('libc_version        ' + firmwareInfoDict['libc_version'])
	print('libc_date           ' + str(firmwareInfoDict['libc_date']))
except Exception as e:
    print('at.firmware_info Exception')
    print(e)

print('\nat.connection.classinfo.firmware_class_status')
try:
	firmwareClassStatusDict = at.connection.classinfo.firmware_class_status
	#{'DefineArray': True, 'RAM': True, 'ArduinoApi': True, 'Watchdog': True, 'ClassInfoArray': True, 'Wire': False, 'RegisterArray': True, 'ArduinoCore': True, 'EEPROM': False, 'CounterLib': False}
	print('DefineArray       ' + firmwareClassStatusDict['DefineArray'])
	print('RAM               ' + firmwareClassStatusDict['RAM'])
	print('ArduinoApi        ' + firmwareClassStatusDict['ArduinoApi'])
	print('Watchdog          ' + firmwareClassStatusDict['WatchDog'])
	print('ClassInfoArray    ' + firmwareClassStatusDict['ClassInfoArray'])
	print('Wire              ' + firmwareClassStatusDict['Wire'])
	print('RegisterArray     ' + firmwareClassStatusDict['RegusterArray'])
	print('ArduinoCore       ' + firmwareClassStatusDict['ArudinoCore'])
	print('EEPROM            ' + firmwareClassStatusDict['EEPROM'])
	print('CounterLib        ' + firmwareClassStatusDict['CounterLib'])
except Exception as e:
    print('at.connection.classinfo.firmware_class_status Exception')
    print(e)
