#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)
#INPUT, OUTPUT = 0, 1
print('aa.HIGH: ' + str(aa.HIGH) + '\taa.LOW: ' + str(aa.LOW))
print('aa.INPUT: ' + str(aa.INPUT) + '\taa.OUTPUT: ' + str(aa.OUTPUT))

inp = ''
while inp != 'q':
	for i in range(2,19+1):
		pin = at.pin.get(i)
		print('Pin: ' + str(i) + '\t\tOutputState: ' + str(pin.digital_value) + '\t\tInputState: ' + str(pin.read_digital_value()) + '\t\tPinMode: '  + str(pin.read_mode()))

	print('')
	print("Which pin to configure? (or 'q' to quit, enter to refresh)")
	inp = input()
	if not (inp == 'q' or inp == ''):
		pinChosen = inp
		print("Change state 's' or pin mode 'p'?")
		inp = input()
		if inp == 's':
			print("High 'h' or low 'l'?")
			inp = input()
			if inp == 'h':
				aa.digitalWrite(pinChosen, aa.HIGH)
			elif inp == 'l':
				aa.digitalWrite(pinChosen, aa.LOW)
			else:
				print('Invalid pin state, returning to pin status menu.')
		elif inp == 'p':
			print("Input 'i' or output 'o'?")
			inp = input()
			if inp == 'i':
				aa.pinMode(pinChosen, aa.INPUT)
			elif inp == 'o':
				aa.pinMode(pinChosen, aa.OUTPUT)
			else:
				print('Invalid pin mode, returning to pin status menu.')
		else:
			print('Invalid option, returning to pin status menu.')



#Soft reset the arduino
#http://www.nongnu.org/avr-libc/user-manual/FAQ.html#faq_softreset
#But it can cause problems...
#https://arduino.stackexchange.com/questions/2922/watchdog-timer-stuck-in-restart-loop-green-led-flashing
##print('at.soft_reset()')
##at.soft_reset()
