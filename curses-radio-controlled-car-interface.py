#!/usr/bin/python3

##########################
## SETTINGS (CONSTANTS) ##
##########################

# Debug settings
KEY_POLL_INTERVAL     = 0.5  # Time delay in seconds between polling the user for key presses which control the vehicle
DEBUG_VERBOSE_MODE    = True # Display extra information in the log
FAKE_AN_ARDUINO       = True # Fake an Arduino on the serial port. This setting disables Nanpy
FAKE_RASPBERRYPI_GPIO = True # Fake Raspberry Pi GPIO pins. This setting disables RPi.GPIO

# Window size settings
CURSES_WINDOW_MIN_X = 126 # Minimum columns required to run interface
CURSES_WINDOW_MIN_Y = 29  # Minimum rows required to run interface

# Nanpy settings
SERIAL_PORT = '/dev/serial0' # Serial port where the Arudino is located for Nanpy

# Raspberry Pi GPIO pins
RPI_I2C_SDA               = 2
RPI_I2C_SCL               = 3
SPEAKER_1_GPIO            = 12
SPEAKER_2_GPIO            = 13
HULL_INDICATOR_LEFT_GPIO  = 27
HULL_INDICATOR_RIGHT_GPIO = 23
GUN_FIRE_GPIO             = 24
RPI_UART_TX               = 14
RPI_UART_RX               = 15
RPI_DTR                   = 17

# Arduino pins
GUN_FIRE_READY_PIN            = 2
TURRET_LIGHTS_PIN             = 3
CAMERA_IR_CONTROL_PIN         = 11
BATTERY_VOLTAGE_LIION_RPI_PIN = 20 #A6
BATTERY_VOLTAGE_LIION_1X3_PIN = 17 #A3
BATTERY_VOLTAGE_LIION_2X3_PIN = 21 #A7

TRACK_RIGHT_PWM_PIN      = 10
TRACK_RIGHT_FORWARD_PIN  = 13
TRACK_RIGHT_BACKWARD_PIN = 14 #(A0)
TRACK_LEFT_PWM_PIN       = 6
TRACK_LEFT_FORWARD_PIN   = 16 #(A2)
TRACK_LEFT_BACKWARD_PIN  = 15 #(A1)

TURRET_X_PWM_PIN = 5
TURRET_LEFT_PIN  = 7
TURRET_RIGHT_PIN = 4
TURRET_Y_PWM_PIN = 9
TURRET_UP_PIN    = 12
TURRET_DOWN_PIN  = 8


######################
## GLOBAL VARIABLES ##
######################

logY = 3
logTotal = 1
mainLoop = True

# Vehicle states
stateTracksLeft  = 0 # 0 = stopped. -1 = backwards.      1 = forwards
stateTracksRight = 0 # 0 = stopped. -1 = backwards.      1 = forwards
stateTurretHoriz = 0 # 0 = stopped. -1 = anti-clockwise. 1 = clockwise
stateTurretVert  = 0 # 0 = stopped. -1 = down.           1 = up

stateHullIndicatorLeft  = False
stateHullIndicatorRight = False
stateGunFiring          = False
stateTurretLights       = False
stateCameraIR           = False

#############
## IMPORTS ##
#############

if not FAKE_AN_ARDUINO:
	import nanpy, nanpy.arduinotree

if not FAKE_RASPBERRYPI_GPIO:
	import RPi.GPIO as GPIO

import curses, time


#############################
## ARDUINO NANPY FUNCTIONS ##
#############################

def trackLeftForward(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.HIGH)
		aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
		aa.analogWrite(TRACK_LEFT_PWM_PIN, speed)
def trackLeftBackward(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.HIGH)
		aa.analogWrite(TRACK_LEFT_PWM_PIN, speed)
def trackLeftStop():
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
		aa.analogWrite(TRACK_LEFT_PWM_PIN, 0)

def trackRightForward(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.HIGH)
		aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
		aa.analogWrite(TRACK_RIGHT_PWM_PIN, speed)
def trackRightBackward(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.HIGH)
		aa.analogWrite(TRACK_RIGHT_PWM_PIN, speed)
def trackRightStop():
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
		aa.analogWrite(TRACK_RIGHT_PWM_PIN, 0)

def turretLeft(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_LEFT_PIN, aa.HIGH)
		aa.digitalWrite(TURRET_RIGHT_PIN, aa.LOW)
		aa.analogWrite(TURRET_X_PWM_PIN, speed)
def turretRight(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_LEFT_PIN, aa.LOW)
		aa.digitalWrite(TURRET_RIGHT_PIN, aa.HIGH)
		aa.analogWrite(TURRET_X_PWM_PIN, speed)
def turretXStop():
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_LEFT_PIN, aa.LOW)
		aa.digitalWrite(TURRET_RIGHT_PIN, aa.LOW)
		aa.analogWrite(TURRET_X_PWM_PIN, 0)

def turretUp(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_UP_PIN, aa.HIGH)
		aa.digitalWrite(TURRET_DOWN_PIN, aa.LOW)
		aa.analogWrite(TURRET_Y_PWM_PIN, speed)
def turretDown(speed):
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_UP_PIN, aa.LOW)
		aa.digitalWrite(TURRET_DOWN_PIN, aa.HIGH)
		aa.analogWrite(TURRET_Y_PWM_PIN, speed)
def turretYStop():
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TURRET_UP_PIN, aa.LOW)
		aa.digitalWrite(TURRET_DOWN_PIN, aa.LOW)
		aa.analogWrite(TURRET_Y_PWM_PIN, 0)

def fireGun():
	pass #Firing gun not implemented

def arduinoSetupPins():
	if not FAKE_AN_ARDUINO:
		#printToLogDebug('Setting up pins')
		#aa.pinMode(TRACK_LEFT_PWM_PIN, aa.OUTPUT)
		#aa.pinMode(TRACK_LEFT_FORWARD_PIN, aa.OUTPUT)
		#aa.pinMode(TRACK_LEFT_BACKWARD_PIN, aa.OUTPUT)
		#aa.pinMode(TRACK_RIGHT_PWM_PIN, aa.OUTPUT)
		aa.pinMode(TRACK_RIGHT_FORWARD_PIN, aa.OUTPUT)
		#aa.pinMode(TRACK_RIGHT_BACKWARD_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_X_PWM_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_LEFT_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_RIGHT_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_Y_PWM_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_UP_PIN, aa.OUTPUT)
		#aa.pinMode(TURRET_DOWN_PIN, aa.OUTPUT)

def arduinoUnsetPins(): # Set Arduino pins to their default values
	if not FAKE_AN_ARDUINO:
		#printToLogDebug("Setting pins to input, low")
		for i in range(1,20):
			aa.digitalWrite(i, aa.LOW)
			aa.pinMode(i, aa.INPUT)
			time.sleep(0.05)


#################################
## RASPBERRY PI GPIO FUNCTIONS ##
#################################

def gpioUnsetPins(): # Set Raspberry Pi GPIO pins to their default values
	if not FAKE_RASPBERRYPI_GPIO:
		pass

# Work in progress


######################
## CURSES FUNCTIONS ##
######################

def endCurses():
	global curses
	global stdscr

	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()

	print('Curses ended')

def checkCursesWindowSize(window):
	#Minimum size is 126 columns x 29 lines
	y, x = window.getmaxyx()
	if y >= CURSES_WINDOW_MIN_Y and x >= CURSES_WINDOW_MIN_X:
		return True
	else:
		return False

def printButton(window, startY, startX, text, status):
	if status:
		pairID = 5
	else:
		pairID = 4

	window.addstr(startY,   startX, '#'*(len(text)+2)    , curses.color_pair(pairID))
	window.addstr(startY+1, startX, '#' + str(text) + '#', curses.color_pair(pairID))
	window.addstr(startY+2, startX, '#'*(len(text)+2)    , curses.color_pair(pairID))

def printKeysInformation(windowButtonInformation):
	windowButtonInformation.addstr(1,1, 'Keys information')

	curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

	printButton(windowButtonInformation, 2, 2,  'Q', False)
	printButton(windowButtonInformation, 6, 2,  'A', False)

	printButton(windowButtonInformation, 2, 10, 'E', False)
	printButton(windowButtonInformation, 6, 6,  'S', False)
	printButton(windowButtonInformation, 6, 10, 'D', False)
	printButton(windowButtonInformation, 6, 14, 'F', False)

	printButton(windowButtonInformation, 2, 18, 'T', False)
	printButton(windowButtonInformation, 6, 18, 'G', False)

	printButton(windowButtonInformation, 2, 30, 'I', False)
	printButton(windowButtonInformation, 6, 26, 'J', False)
	printButton(windowButtonInformation, 6, 30, 'K', False)
	printButton(windowButtonInformation, 6, 34, 'L', False)

	printButton(windowButtonInformation, 2, 46, '1', False)
	printButton(windowButtonInformation, 2, 50, '2', False)
	printButton(windowButtonInformation, 2, 54, '3', False)
	printButton(windowButtonInformation, 2, 58, '4', False)
	printButton(windowButtonInformation, 2, 62, '5', False)

	printButton(windowButtonInformation, 6, 46, '6', False)
	printButton(windowButtonInformation, 6, 50, '7', False)
	printButton(windowButtonInformation, 6, 54, '8', False)
	printButton(windowButtonInformation, 6, 58, '9', False)
	printButton(windowButtonInformation, 6, 62, '0', False)

	printButton(windowButtonInformation, 2, 74, 'Escape',    False)
	printButton(windowButtonInformation, 6, 74, 'Enter',     False)
	printButton(windowButtonInformation, 2, 83, 'Backspace', False)
	printButton(windowButtonInformation, 6, 83, 'Space',     False)

	windowButtonInformation.refresh()

def printTankModules(windowTankModules):
	windowTankModules.addstr(1,1, 'Tank Modules')

	windowTankModules.addstr(3,  10, '       I')
	windowTankModules.addstr(4,  10, '       I')
	windowTankModules.addstr(5,  10, '       I')
	windowTankModules.addstr(6,  10, '+-#####I#####-+')
	windowTankModules.addstr(7,  10, '| #####I##### |')
	windowTankModules.addstr(8,  10, '| ##xxxxxxx## |')
	windowTankModules.addstr(9,  10, '| #xxxxxxxxx# |')
	windowTankModules.addstr(10, 10, '| #xxxxxxxxx# |')
	windowTankModules.addstr(11, 10, '| ###xxxxx### |')
	windowTankModules.addstr(12, 10, '| ########### |')
	windowTankModules.addstr(13, 10, '| ########### |')
	windowTankModules.addstr(14, 10, '| ########### |')
	windowTankModules.addstr(15, 10, '| ########### |')
	windowTankModules.addstr(16, 10, '+-###########-+')
	windowTankModules.refresh()

def printTankBatteryLevels(windowTankModules, batteryComponents_74Volts, batteryComponents_37Volts, batteryRpi_74Volts):
	batteryComponents_74VoltsPerdec = int((batteryComponents_74Volts - 6) / (0.84 - 0.6))
	batteryComponents_37VoltsPerdec = int((batteryComponents_37Volts - 3) / (0.42 - 0.3))
	batteryRpi_74VoltsPerdec        = int((batteryRpi_74Volts        - 6) / (0.84 - 0.6))

	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
	curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
	for i in range(16, 16-batteryComponents_74VoltsPerdec, -1): #batteryComponents_74Volts
		if i >= 15:
			windowTankModules.addstr(i, 30, chr(9608), curses.color_pair(1))
		elif i >=12:
			windowTankModules.addstr(i, 30, chr(9608), curses.color_pair(2))
		else:
			windowTankModules.addstr(i, 30, chr(9608), curses.color_pair(3))

	for i in range(16, 16-batteryComponents_37VoltsPerdec, -1): #batteryComponents_74Volts
		if i >= 15:
			windowTankModules.addstr(i, 32, chr(9608), curses.color_pair(1))
		elif i >=12:
			windowTankModules.addstr(i, 32, chr(9608), curses.color_pair(2))
		else:
			windowTankModules.addstr(i, 32, chr(9608), curses.color_pair(3))

	for i in range(16, 16-batteryRpi_74VoltsPerdec, -1): #batteryComponents_74Volts
		if i >= 15:
			windowTankModules.addstr(i, 36, chr(9608), curses.color_pair(1))
		elif i >=12:
			windowTankModules.addstr(i, 36, chr(9608), curses.color_pair(2))
		else:
			windowTankModules.addstr(i, 36, chr(9608), curses.color_pair(3))

	windowTankModules.refresh()

def printToLog(windowLog, text):
	global logY, logTotal
	logMaxY, logMaxX = windowLog.getmaxyx()

	windowLog.addstr(logY  , 2, ' '*(logMaxX-4))
	windowLog.addstr(logY+1, 2, ' '*(logMaxX-4))
	windowLog.addstr(logY,   2, '%03d' % (logTotal % 1000) + ': ' + str(text))
	logTotal = logTotal + 1
	windowLog.refresh()

	logY = windowLog.getyx()[0];
	if logY >= logMaxY - 3:
		logY = 3
	else:
		logY = logY + 1

def printToLogDebug(windowLog, text):
	if (DEBUG_VERBOSE_MODE):
		try:
			printToLog(windowLog, 'DEBUG: ' + str(text))
		except Exception as e:
			print("Debug print error occured:")
			print(e)
			print("Text: " + str(text)) # Print text
			time.sleep(2)
		except:
			print("Debug print error")
			print("Text: " + str(text)) # Print text
			time.sleep(2)


##################
## MAIN PROGRAM ##
##################

def main_curses(stdscr):
	global mainLoop # Global variables
	global stateTracksLeft, stateTracksRight, stateTurretHoriz, stateTurretVert, stateHullIndicatorLeft, stateHullIndicatorRight, stateGunFiring, stateTurretLights, stateCameraIR # Global variables - Vehicle states
	if not FAKE_AN_ARDUINO: # Global variables - Nanpy
		global aa, at

	#stdscr = curses.initscr() # setup intial window
	#curses.start_color() # Enable curses colour
	#curses.use_default_colors() # Use default curses colours
	curses.noecho()        # Don't echo keystrokes
	curses.cbreak()        # Don't wait for enter, handle keys immediately
	stdscr.keypad(True)    # Use aliases for special keys
	curses.curs_set(False) # Suppress the blinking cursor
	stdscr.nodelay(True)   # Set getch() and getkey() to non-blocking

	if checkCursesWindowSize(stdscr):
		y, x = stdscr.getmaxyx()
		stdscr.refresh()

		# Windows setup
		#newwin(int nlines, int ncols, int begin_y, intbegin_x)
		windowLog = curses.newwin(y-10, int(x/2), 0, int(x/2))
		windowLog.addstr(1,1, 'Log')
		windowLog.border()
		windowLog.refresh()

		windowTankModules = curses.newwin(y-10, int(x/2), 0, 0)
		windowTankModules.box()
		windowTankModules.refresh()
		printTankModules(windowTankModules)

		windowButtonInformation = curses.newwin(10, x, y-10, 0)
		windowButtonInformation.box()
		windowButtonInformation.refresh()
		printKeysInformation(windowButtonInformation)

		stdscr.refresh()

		printToLog(windowLog, 'Curses started')
		printToLogDebug(windowLog, 'Terminal size: ' + str(x) + 'x' + str(y))
		printTankBatteryLevels(windowTankModules, 8.4, 3.2, 7.4) # Testing

		if not FAKE_AN_ARDUINO:
			connection = nanpy.SerialManager(device=SERIAL_PORT)
			aa = nanpy.ArduinoApi(connection=connection)
			at = nanpy.arduinotree.ArduinoTree(connection=connection)

		# Main program loop
		while mainLoop:
			time.sleep(KEY_POLL_INTERVAL)

			# Vehicle states checking code
			if stateHullIndicatorLeft:
				pass
			if stateHullIndicatorRight:
				pass
			if stateGunFiring:
				#fireGun()
				pass
			if stateTurretLights:
				pass
			if stateCameraIR:
				pass

			if stateTracksLeft == -1:
				printToLogDebug(windowLog, 'Left track backward')
				trackLeftBackward(255) # Set left track motion
			if stateTracksLeft == 0:
				printToLogDebug(windowLog, 'Left track stopped')
				trackLeftStop() # Stop all left track motion
			if stateTracksLeft == 1:
				printToLogDebug(windowLog, 'Left track forward')
				trackLeftForward(255) # Set left track motion

			if stateTracksRight == -1:
				printToLogDebug(windowLog, 'Right track backward')
				trackRightBackward(255) # Set right track motion
			if stateTracksRight == 0:
				printToLogDebug(windowLog, 'Right track stopped')
				trackRightStop() # Stop all right track motion
			if stateTracksRight == 1:
				printToLogDebug(windowLog, 'Right track forward')
				trackRightForward(255) # Set right track motion

			if stateTurretHoriz == -1:
				printToLogDebug(windowLog, 'Turret horiz left')
				turretLeft(255) # Set turret horizontal motion
			if stateTurretHoriz == 0:
				printToLogDebug(windowLog, 'Turret horiz stopped')
				turretXStop() # Stop all horizontal turret motion
			if stateTurretHoriz == 1:
				printToLogDebug(windowLog, 'Turret horiz right')
				turretRight(255) # Set turret horizontal motion

			if stateTurretVert == -1:
				printToLogDebug(windowLog, 'Turret vert down')
				turretDown(255) # Set turret vertical motion
			if stateTurretVert == 0:
				printToLogDebug(windowLog, 'Turret vert stopped')
				turretYStop() # Stop all vertical turret motion
			if stateTurretVert == 1:
				printToLogDebug(windowLog, 'Turret vert up')
				turretUp(255) # Set turret vertical motion


			# Key input code
			key = stdscr.getch()
			#curses.flushinp()
			if key != curses.ERR:
				#stdscr.refresh()
				if key == 27: # Esc key - quit
					arduinoUnsetPins()
					gpioUnsetPins()
					printToLog(windowLog, 'All movement stopped and modules offline')
					printToLog(windowLog, 'Are you sure you want to quit? (y/n)')
					stdscr.nodelay(False) # Set getch() and getkey() to blocking
					key = stdscr.getch()
					stdscr.refresh()
					if key == ord('y'):
						mainLoop = False # The 'break' in the line below will exit the loop, but setting this variable is a backup
						stdscr.nodelay(True) # set getch() and getkey() to non-blocking
						break # Exit the loop
					stdscr.nodelay(True) # set getch() and getkey() to non-blocking
				elif key == 263: # Backspace key - abort all movement + modules. Reset pins to their default state
					printToLog(windowLog, 'All movement stopped and modules offline')
					arduinoUnsetPins()
					gpioUnsetPins()
					stateTracksLeft = 0
					stateTracksRight = 0
					stateTurretHoriz = 0
					stateTurretVert = 0
					stateHullIndicatorLeft = False
					stateHullIndicatorRight = False
					stateGunFiring = False
					stateTurretLights = False
					stateCameraIR = False
				elif key == 32: # Space bar - fire gun
					stateGunFiring = True
				elif key == ord('q'):
					if stateTracksRight == 1:
						stateTracksRight = 0
					else:
						stateTracksRight = 1
				elif key == ord('a'):
					if stateTracksRight == -1:
						stateTracksRight = 0
					else:
						stateTracksRight = -1
				elif key == ord('e'):
					if stateTracksLeft == 1 and stateTracksRight == 1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = 1
						stateTracksRight = 1
				elif key == ord('s'):
					if stateTracksLeft == -1 and stateTracksRight == 1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = -1
						stateTracksRight = 1
				elif key == ord('d'):
					if stateTracksLeft == -1 and stateTracksRight == -1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = -1
						stateTracksRight = -1
				elif key == ord('f'):
					if stateTracksLeft == 1 and stateTracksRight == -1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = 1
						stateTracksRight = -1
				elif key == ord('t'):
					if stateTracksLeft == 1:
						stateTracksLeft = 0
					else:
						stateTracksLeft = 1
				elif key == ord('g'):
					if stateTracksLeft == -1:
						stateTracksLeft = 0
					else:
						stateTracksLeft = -1
				elif key == ord('i'):
					if stateTurretVert == 1:
						stateTurretVert = 0
					else:
						stateTurretVert = 1
				elif key == ord('j'):
					if stateTurretHoriz == -1:
						stateTurretHoriz = 0
					else:
						stateTurretHoriz = -1
				elif key == ord('k'):
					if stateTurretVert == -1:
						stateTurretVert = 0
					else:
						stateTurretVert = -1
				elif key == ord('l'):
					if stateTurretHoriz == 1:
						stateTurretHoriz = 0
					else:
						stateTurretHoriz = 1
				else:
					printToLog(windowLog, 'Warning: Pressed key not recognised: ' + chr(key) + ' = ' + str(key))

			else:
				printToLogDebug(windowLog, 'No key pressed')

			key = -1
	else:
		endCurses()
		print('Curses window is too small')
		print('Minimum size is ' + str(CURSES_WINDOW_MIN_X) + ' rows by ' + str(CURSES_WINDOW_MIN_Y) + ' lines')
		print('Current size is ' + str(stdscr.getmaxyx()[1]) + ' rows by ' + str(stdscr.getmaxyx()[0]) + ' lines')

if __name__ == "__main__":
	try:
		curses.wrapper(main_curses)
	except Exception as e:
	#except RuntimeError as e:
		arduinoUnsetPins()
		gpioUnsetPins()
		print('Exception')
		print(e)
	except KeyboardInterrupt as e:
		arduinoUnsetPins()
		gpioUnsetPins()
		print('KeyboardInterrupt')
		print(e)
	except:
		arduinoUnsetPins()
		gpioUnsetPins()

	arduinoUnsetPins()
	gpioUnsetPins()
