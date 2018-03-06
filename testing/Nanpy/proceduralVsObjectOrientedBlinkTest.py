#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')

aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

INPUT, OUTPUT = 0, 1
PIN_NUMBER = 13 #Arduino pin number used for this test. PIN_NUMBER = 13 here a.k.a. LED_BUILTIN

#### Procedural code ####
aa.pinMode(PIN_NUMBER, aa.OUTPUT)
aa.digitalWrite(PIN_NUMBER, aa.HIGH)
print("P-H: pin.digital_value: " + str(pin.digital_value))
print("P-H: pin.read_digital_value(): " + str(pin.read_digital_value()))

aa.pinMode(PIN_NUMBER, aa.OUTPUT)
aa.digitalWrite(PIN_NUMBER, aa.LOW)
print("P-L: pin.digital_value: " + str(pin.digital_value))
print("P-L: pin.read_digital_value(): " + str(pin.read_digital_value()))

#### Object-oriented code ####
pin = at.pin.get(PIN_NUMBER)
pin.reset()

pin.write_mode(OUTPUT)
pin.write_digital_value(1)
time.sleep(1)
print("OO-WDV-H: pin.read_digital_value(): " + str(pin.read_digital_value()))
print("OO-WDV-H: pin.digital_value: " + str(pin.digital_value))
print("OO-WDV-H: pin.read_mode(): " + str(pin.read_mode()))

pin.write_mode(OUTPUT)
pin.write_digital_value(0)
time.sleep(1)
print("OO-WDV-L: pin.digital_value: " + str(pin.digital_value))
print("OO-WDV-L: pin.read_digital_value(): " + str(pin.read_digital_value()))
print("OO-WDV-L: pin.read_mode(): " + str(pin.read_mode()))

pin.write_pullup(True)
time.sleep(1)
print("OO-WPU-H: pin.digital_value: " + str(pin.digital_value))
print("OO-WPU-H: pin.read_digital_value(): " + str(pin.read_digital_value()))
print("OO-WPU-H: pin.read_mode(): " + str(pin.read_mode()))

pin.write_pullup(False)
time.sleep(1)
print("OO-WPU-L: pin.digital_value: " + str(pin.digital_value))
print("OO-WPU-L: pin.read_digital_value(): " + str(pin.read_digital_value()))
print("OO-WPU-L: pin.read_mode(): " + str(pin.read_mode()))


aa.pinMode(PIN_NUMBER, aa.INPUT)
aa.digitalWrite(PIN_NUMBER, aa.LOW)
