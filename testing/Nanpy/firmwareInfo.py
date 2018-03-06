#!/usr/bin/python3
import time, nanpy
import nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

firmwareInfoDict = at.firmware_info

print('avr_name            ' + firmwareInfoDict['avr_name'])
print('arduino_version     ' + firmwareInfoDict['arduino_version'])
print('compile_datetime    ' + str(firmwareInfoDict['compile_datetime']))
print('gcc_version         ' + firmwareInfoDict['gcc_version'])
print('libc_version        ' + firmwareInfoDict['libc_version'])
print('libc_date           ' + str(firmwareInfoDict['libc_date']))
