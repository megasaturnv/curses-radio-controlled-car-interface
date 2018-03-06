#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree

try:
    import readline
except:
    pass #readline not available

connection = nanpy.SerialManager(device='/dev/serial0')

aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

INPUT, OUTPUT = 0, 1
inp = ""

while inp != "q":
	inp = input("Enter the pin number you wish to see information about ( 0 - 21 ). Type 'q' to quit > ")

	if inp != "q":
		i = int(inp)
		pin = at.pin.get(i)
		print(str(i) + ": ==== Global Vars ====")
	#	print("at.pin.get(): " + str(at.pin.get()))
		print("    " + str(i) + ": at.pin.count:             " + str(at.pin.count))
		print("    " + str(i) + ": at.pin.count_digital:     " + str(at.pin.count_digital))
		print("    " + str(i) + ": at.pin.count_analog:      " + str(at.pin.count_analog))
	#	print("at.pin.get.range_all: " + str(at.pin.get.range_all, range(0, 20)))
	#	print("at.pin.get.range_analog" + str(at.pin.get.range_analog, range(14, 20)))
	#	print("at.pin.get.range_digital" + str(at.pin.get.range_digital, range(0, 14)))

		print(str(i) + ": ==== Static pin info ====")
		print("    " + str(i) + ": pin number:               " + str(pin.pin_number))
		print("    " + str(i) + ": analog pin number:        " + str(pin.pin_number_analog))

		print("    " + str(i) + ": at.pin.get(i).is_digital: " + str(at.pin.get(i).is_digital))
		print("    " + str(i) + ": at.pin.get(i).is_analog:  " + str(at.pin.get(i).is_analog))
		print("    " + str(i) + ": at.pin.get(i).name:       " + str(at.pin.get(i).name))

		print(str(i) + ": ==== Dynamic pin info ====")
		print("    " + str(i) + ": pin.mode:                 " + str(pin.mode))
		print("    " + str(i) + ": pin.read_mode():          " + str(pin.read_mode()))
		print("    " + str(i) + ": pin.read_digital_value(): " + str(pin.read_digital_value()))
		print("    " + str(i) + ": pin.digital_value:        " + str(pin.digital_value))

		print(str(i) + ": ==== Port Registers ====")
		print("    " + str(i) + ": D=00-07 B=08-13 C=A0-A7")
		print("    " + str(i) + ": DDRD:                     " + '{0:08b}'.format(at.register.get('DDRD').value)  + "    " + str(at.register.get('DDRD').value))
		print("    " + str(i) + ": PORTD:                    " + '{0:08b}'.format(at.register.get('PORTD').value) + "    " + str(at.register.get('PORTD').value))
		print("    " + str(i) + ": PIND:                     " + '{0:08b}'.format(at.register.get('PIND').value)  + "    " + str(at.register.get('PIND').value))
		print("    " + str(i) + ": DDRB:                     " + '{0:08b}'.format(at.register.get('DDRB').value)  + "    " + str(at.register.get('DDRD').value))
		print("    " + str(i) + ": PORTB:                    " + '{0:08b}'.format(at.register.get('PORTB').value) + "    " + str(at.register.get('PORTB').value))
		print("    " + str(i) + ": PINB:                     " + '{0:08b}'.format(at.register.get('PINB').value)  + "    " + str(at.register.get('PINB').value))
		print("    " + str(i) + ": DDRC:                     " + '{0:08b}'.format(at.register.get('DDRC').value)  + "    " + str(at.register.get('DDRC').value))
		print("    " + str(i) + ": PORTC:                    " + '{0:08b}'.format(at.register.get('PORTC').value) + "    " + str(at.register.get('PORTC').value))
		print("    " + str(i) + ": PINC:                     " + '{0:08b}'.format(at.register.get('PINC').value)  + "    " + str(at.register.get('PINC').value))

		time.sleep(0.25)
		pin.reset()
		print(str(i) + ": ==== pin.reset() ====")
		time.sleep(0.25)
		print("    " + str(i) + ": pin.mode:                 " + str(pin.mode))
		print("    " + str(i) + ": pin.read_mode():          " + str(pin.read_mode()))
