#!/usr/bin/python3
import time, nanpy
import nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

print ('uptime: %s sec' % (at.api.millis() / 1000.0))
