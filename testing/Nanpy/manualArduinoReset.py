#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

#INPUT, OUTPUT = 0, 1

#Soft reset the arduino
#http://www.nongnu.org/avr-libc/user-manual/FAQ.html#faq_softreset
#But it can cause problems...
#https://arduino.stackexchange.com/questions/2922/watchdog-timer-stuck-in-restart-loop-green-led-flashing
##print('at.soft_reset()')
##at.soft_reset()

#Reset to the pin to a safe default state: INPUT, no pullup. PWM reset.
def manualReset(pinobj):
	pinobj.write_mode(INPUT)
	pinobj.write_pullup(LOW)
	if pinobj.pwm.available:
		pinobj.pwm.reset()

#Use nanpy's reset function. This may be functionally equivelant to the function above - need to check nanpy source code
def nanpyReset(pinobj):
	#reset the pin with nanpy's per-pin built-in reset
	pinobj.reset()

for i in range(2, 19+1): # Pin 2 - 13, A0 - A5 (Not A6 & A7)
	pin = at.pin.get(i)
	Print('Pin: ' + str(i) + '\t\tOutputState: ' + str(pin.digital_value) + '\t\tInputState: ' + str(pin.read_digital_value()) + '\t\tPinMode: '  + str(pin.read_mode()))

for i in range(2, 19+1): # Pin 2 - 13, A0 - A5 (Not A6 & A7)
	pin = at.pin.get(i)
	#manualReset(pin)
	nanpyReset(pin)

for i in range(2, 19+1): # Pin 2 - 13, A0 - A5 (Not A6 & A7)
	pin = at.pin.get(i)
	Print('Pin: ' + str(i) + '\t\tOutputState: ' + str(pin.digital_value) + '\t\tInputState: ' + str(pin.read_digital_value()) + '\t\tPinMode: '  + str(pin.read_mode()))
