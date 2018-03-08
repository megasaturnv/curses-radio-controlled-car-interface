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

# Speed and acceleration settings
TRACK_RIGHT_SPEED_1_PWM  = 150 # Track speeds. Value = 0 - 255
TRACK_RIGHT_SPEED_2_PWM  = 200
TRACK_RIGHT_SPEED_3_PWM  = 255
TRACK_LEFT_SPEED_1_PWM  = 150
TRACK_LEFT_SPEED_2_PWM  = 200
TRACK_LEFT_SPEED_3_PWM  = 255

TRACK_LEFT_SLOW_ACCELERATION_FACTOR  = 80 # Acceleration in (PWM units / second) for left track
TRACK_RIGHT_SLOW_ACCELERATION_FACTOR = 80 # Acceleration in (PWM units / second) for right track

# Nanpy settings
SERIAL_PORT = '/dev/serial0' # Serial port where the Arudino is located for Nanpy

# Arduino pins
BBGUN_FIRE_READY_PIN          = 2
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

TURRET_LEFT_SPEED_PWM  = 255
TURRET_RIGHT_SPEED_PWM = 255
TURRET_UP_SPEED_PWM    = 255
TURRET_DOWN_SPEED_PWM  = 255

# Raspberry Pi GPIO pins
RPI_I2C_SDA               = 2
RPI_I2C_SCL               = 3
SPEAKER_1_GPIO            = 12
SPEAKER_2_GPIO            = 13
HULL_INDICATOR_LEFT_GPIO  = 27
HULL_INDICATOR_RIGHT_GPIO = 23
BBGUN_FIRE_GPIO           = 24
RPI_UART_TX               = 14
RPI_UART_RX               = 15
RPI_DTR                   = 17


######################
## GLOBAL VARIABLES ##
######################

logY = 3
logTotal = 1
mainLoop = True

stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_3_PWM
stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_3_PWM
stateTracksAcceleration = 2


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

def trackLeftSpeed(speed):
	if not FAKE_AN_ARDUINO:
		aa.analogWrite(TRACK_LEFT_PWM_PIN, abs(speed)) # Set track's speed on PWM pin. abs() is used to make sure the number isn't negative
def trackLeft(velocity):
	if not FAKE_AN_ARDUINO:
		aa.analogWrite(TRACK_LEFT_PWM_PIN, abs(velocity))  # Set track's absolute velocity (speed) on PWM pin
		if velocity == 0: # Set tracks to not move
			aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
			aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
		elif velocity > 0: # Set tracks to move forwards
			aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.HIGH)
			aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
		elif velocity < 0: # Set tracks to move backwards
			aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
			aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.HIGH)

def trackRightSpeed(speed):
	if not FAKE_AN_ARDUINO:
		aa.analogWrite(TRACK_RIGHT_PWM_PIN, abs(speed)) # Set track's speed on PWM pin. abs() is used to make sure the number isn't negative
def trackRight(velocity):
	if not FAKE_AN_ARDUINO:
		aa.analogWrite(TRACK_RIGHT_PWM_PIN, abs(velocity)) # Set track's absolute velocity (speed) on PWM pin
		if velocity == 0: # Set tracks to not move
			aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
			aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
		elif velocity > 0: # Set tracks to move forwards
			aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.HIGH)
			aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
		elif velocity < 0: # Set tracks to move backwards
			aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
			aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.HIGH)

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

def fireBBGun():
	pass #Firing BB gun not implemented

def arduinoSetupPinsState(): # Setup Arduino pins' state to their default values
	if not FAKE_AN_ARDUINO:
		aa.digitalWrite(TRACK_LEFT_PWM_PIN, aa.LOW)
		aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_RIGHT_PWM_PIN, aa.LOW)
		aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
		aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
		aa.digitalWrite(TURRET_X_PWM_PIN, aa.LOW)
		aa.digitalWrite(TURRET_LEFT_PIN, aa.LOW)
		aa.digitalWrite(TURRET_RIGHT_PIN, aa.LOW)
		aa.digitalWrite(TURRET_Y_PWM_PIN, aa.LOW)
		aa.digitalWrite(TURRET_UP_PIN, aa.LOW)
		aa.digitalWrite(TURRET_DOWN_PIN, aa.LOW)

def arduinoSetupPinsMode(): # Setup Arduino pins' mode to their default values
	if not FAKE_AN_ARDUINO:
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

def arduinoResetPins(): # Reset all Arduino pins to safe values (INPUT, LOW)
	if not FAKE_AN_ARDUINO:
		#printToLogDebug("Setting pins to input, low")
		for i in range(1,20):
			aa.digitalWrite(i, aa.LOW)
			aa.pinMode(i, aa.INPUT)
			time.sleep(0.05)


#################################
## RASPBERRY PI GPIO FUNCTIONS ##
#################################

def rpiGpioSetupPinsState(): # Setup Raspberry Pi GPIO state to their default values
	if not FAKE_RASPBERRYPI_GPIO:
		pass

def rpiGpioSetupPinsMode(): # Setup Raspberry Pi GPIO mode to their default values
	if not FAKE_RASPBERRYPI_GPIO:
		pass

def rpiGpioResetPins(): # Reset all Raspberry Pi GPIO pins to safe values (INPUT, LOW)
	if not FAKE_RASPBERRYPI_GPIO:
		pass

# Not yet implemented. Work in progress


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
	# Global variables
	global mainLoop
	global stateTracksLeft, stateTracksRight, stateTurretHoriz, stateTurretVert, stateHullIndicatorLeft, stateHullIndicatorRight, stateBBGunFiring, stateTurretLights, stateCameraIR, stateLeftTracksTargetSpeed, stateRightTracksTargetSpeed, stateTracksAcceleration # Global variables - Vehicle states
	if not FAKE_AN_ARDUINO: # Global variables - Nanpy
		global aa, at

	# Local variables
	stateTracksLeft  = 0 # Direction track is trying to move. 0 = stop motor. -1 = backwards.      1 = forwards.  1000 = null state, no command sent to Arduino.
	stateTracksRight = 0 # Direction track is trying to move. 0 = stop motor. -1 = backwards.      1 = forwards.  1000 = null state, no command sent to Arduino.
	stateTurretHoriz = 0 # Direction track is trying to move. 0 = stop motor. -1 = anti-clockwise. 1 = clockwise. 1000 = null state, no command sent to Arduino.
	stateTurretVert  = 0 # Direction track is trying to move. 0 = stop motor. -1 = down.           1 = up.        1000 = null state, no command sent to Arduino.
	stateHullIndicatorLeft  = False
	stateHullIndicatorRight = False
	stateBBGunFiring        = False
	stateTurretLights       = False
	stateCameraIR           = False
	stateLeftTracksCurrentVelocity = 0
	stateRightTracksCurrentVelocity = 0
	trackAccelerationLastSet = time.time()

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

		arduinoSetupPinsState() # Set all pins to their defaults
		arduinoSetupPinsMode()
		rpiGpioSetupPinsState()
		rpiGpioSetupPinsMode()

		# Main program loop
		while mainLoop:
			time.sleep(KEY_POLL_INTERVAL)

			# Velocity and acceleration calculation code
			if stateTracksAcceleration == 1: # If stateTracksAcceleration == 1, accelerate slowly
				elapsedTime = time.time() - trackAccelerationLastSet # Calculate elapsed time in seconds since the last time the track's velocity was updated

				# Velocity and acceleration calculation code - Left track
				if stateTracksLeft == 1: # If track is trying to move forward
					stateLeftTracksCurrentVelocity += int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime to stateLeftTracksCurrentVelocity
					if abs(stateLeftTracksCurrentVelocity) > stateLeftTracksTargetSpeed: # If current speed is larger than target speed
						stateLeftTracksCurrentVelocity = stateLeftTracksTargetSpeed # Set current velocity to positive target speed
				elif stateTracksLeft == -1: # If track is trying to move backward
					stateLeftTracksCurrentVelocity -= int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime from stateLeftTracksCurrentVelocity
					if abs(stateLeftTracksCurrentVelocity) > stateLeftTracksTargetSpeed: # If current speed is larger than target speed
						stateLeftTracksCurrentVelocity = -stateLeftTracksTargetSpeed # Set current velocity to negative target speed
				elif stateTracksLeft == 0: # If track is stopping / stopped
					if stateLeftTracksCurrentVelocity > 0: # If stateLeftTracksCurrentVelocity is positive
						stateLeftTracksCurrentVelocity -= int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime from stateLeftTracksCurrentVelocity
						if stateLeftTracksCurrentVelocity < 0: # If above calculation set stateLeftTracksCurrentVelocity to a negative value...
							stateLeftTracksCurrentVelocity = 0 # Set stateLeftTracksCurrentVelocity to 0
					elif stateLeftTracksCurrentVelocity < 0: # If stateLeftTracksCurrentVelocity is negative
						stateLeftTracksCurrentVelocity += int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime to stateLeftTracksCurrentVelocity
						if stateLeftTracksCurrentVelocity > 0: # If above calculation set stateLeftTracksCurrentVelocity to a negative value...
							stateLeftTracksCurrentVelocity = 0 # Set stateLeftTracksCurrentVelocity to 0

				# Velocity and acceleration calculation code - Right track
				if stateTracksRight == 1: # If track is trying to move forward
					stateRightTracksCurrentVelocity += int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime to stateRightTracksCurrentVelocity
					if abs(stateRightTracksCurrentVelocity) > stateRightTracksTargetSpeed: # If current speed is larger than target speed
						stateRightTracksCurrentVelocity = stateRightTracksTargetSpeed # Set current velocity to positive target speed
				elif stateTracksRight == -1: # If track is trying to move backward
					stateRightTracksCurrentVelocity -= int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime from stateRightTracksCurrentVelocity
					if abs(stateRightTracksCurrentVelocity) > stateRightTracksTargetSpeed: # If current speed is larger than target speed
						stateRightTracksCurrentVelocity = -stateRightTracksTargetSpeed # Set current velocity to negative target speed
				elif stateTracksRight == 0: # If track is stopping / stopped
					if stateRightTracksCurrentVelocity > 0: # If stateRightTracksCurrentVelocity is positive
						stateRightTracksCurrentVelocity -= int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime from stateRightTracksCurrentVelocity
						if stateRightTracksCurrentVelocity < 0: # If above calculation set stateRightTracksCurrentVelocity to a negative value...
							stateRightTracksCurrentVelocity = 0 # Set stateRightTracksCurrentVelocity to 0
					elif stateRightTracksCurrentVelocity < 0: # If stateRightTracksCurrentVelocity is negative
						stateRightTracksCurrentVelocity += int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime to stateRightTracksCurrentVelocity
						if stateRightTracksCurrentVelocity > 0: # If above calculation set stateRightTracksCurrentVelocity to a negative value...
							stateRightTracksCurrentVelocity = 0 # Set stateRightTracksCurrentVelocity to 0

			elif stateTracksAcceleration == 2: # If stateTracksAcceleration == 2...
				# Left tracks
				if stateTracksLeft == 1: # If track is trying to move forward...
					stateLeftTracksCurrentVelocity = stateLeftTracksTargetSpeed # Set current velocity to positive target speed instantly
				if stateTracksLeft == -1: # If track is trying to move backward...
					stateLeftTracksCurrentVelocity = -stateLeftTracksTargetSpeed # Set current velocity to negative target speed instantly
				elif stateTracksLeft == 0: # If track is stopping / stopped...
					stateLeftTracksCurrentVelocity = 0 # Set current velocity to 0 instantly

				# Right tracks
				if stateTracksRight == 1: # If track is trying to move forward...
					stateRightTracksCurrentVelocity = stateRightTracksTargetSpeed # Set current velocity to positive target speed instantly
				if stateTracksRight == -1: # If track is trying to move backward...
					stateRightTracksCurrentVelocity = -stateRightTracksTargetSpeed # Set current velocity to negative target speed instantly
				elif stateTracksRight == 0: # If track is stopping / stopped...
					stateRightTracksCurrentVelocity = 0 # Set current velocity to 0 instantly

			trackAccelerationLastSet = time.time() # Set trackAccelerationLastSet to current Unix time

			# Vehicle states checking code
			if stateHullIndicatorLeft:
				stateHullIndicatorLeft = False
			if stateHullIndicatorRight:
				stateHullIndicatorRight = False
			if stateTurretLights:
				stateTurretLights = False
			if stateCameraIR:
				stateCameraIR = False
			if stateBBGunFiring:
				#fireBBGun()
				stateBBGunFiring = False

			if stateTracksLeft == -1:
				printToLogDebug(windowLog, 'Left track velocity: ' + str(stateLeftTracksCurrentVelocity))
				trackLeft(stateLeftTracksCurrentVelocity) # Set left track motion
			elif stateTracksLeft == 0:
				if stateLeftTracksCurrentVelocity == 0:
					trackLeft(0) # Stop all left track motion
					printToLogDebug(windowLog, 'Left track stopped')
					stateTracksLeft = 1000
				else:
					trackLeftSpeed(abs(stateLeftTracksCurrentVelocity)) # Set left track pwm speed to stateLeftTracksCurrentVelocity
					printToLogDebug(windowLog, 'Left track stopping. Velocity: ' + str(stateLeftTracksCurrentVelocity))
			elif stateTracksLeft == 1:
				printToLogDebug(windowLog, 'Left track velocity: ' + str(stateLeftTracksCurrentVelocity))
				trackLeft(stateLeftTracksCurrentVelocity) # Set left track motion

			if stateTracksRight == -1:
				printToLogDebug(windowLog, 'Right track velocity: ' + str(stateRightTracksCurrentVelocity))
				trackRight(stateRightTracksCurrentVelocity) # Set right track motion
			elif stateTracksRight == 0:
				if stateRightTracksCurrentVelocity == 0:
					trackRight(0) # Stop all right track motion
					printToLogDebug(windowLog, 'Right track stopped')
					stateTracksRight = 1000
				else:
					trackRightSpeed(abs(stateRightTracksCurrentVelocity)) # Set right track pwm speed to stateRightTracksCurrentVelocity
					printToLogDebug(windowLog, 'Right track stopping. Velocity: ' + str(stateRightTracksCurrentVelocity))
			elif stateTracksRight == 1:
				printToLogDebug(windowLog, 'Right track velocity: ' + str(stateRightTracksCurrentVelocity))
				trackRight(stateRightTracksCurrentVelocity) # Set right track motion

			if stateTurretHoriz == -1:
				printToLogDebug(windowLog, 'Turret horiz left')
				turretLeft(TURRET_LEFT_SPEED_PWM) # Set turret horizontal motion
			elif stateTurretHoriz == 0:
				printToLogDebug(windowLog, 'Turret horiz stopped')
				turretXStop() # Stop all horizontal turret motion
				stateTurretHoriz = 1000
			elif stateTurretHoriz == 1:
				printToLogDebug(windowLog, 'Turret horiz right')
				turretRight(TURRET_RIGHT_SPEED_PWM) # Set turret horizontal motion

			if stateTurretVert == -1:
				printToLogDebug(windowLog, 'Turret vert down')
				turretDown(TURRET_DOWN_SPEED_PWM) # Set turret vertical motion
			elif stateTurretVert == 0:
				printToLogDebug(windowLog, 'Turret vert stopped')
				turretYStop() # Stop all vertical turret motion
				stateTurretVert = 1000
			elif stateTurretVert == 1:
				printToLogDebug(windowLog, 'Turret vert up')
				turretUp(TURRET_UP_SPEED_PWM) # Set turret vertical motion


			# Key input code
			key = stdscr.getch()
			#curses.flushinp()
			if key != curses.ERR:
				#stdscr.refresh()
				if key == 27: # Esc key - quit
					arduinoSetupPinsState() # Set all pins to their defaults
					arduinoSetupPinsMode()
					rpiGpioSetupPinsState()
					rpiGpioSetupPinsMode()

					stateTracksLeft = 0 # Set state variables to their non-functional values
					stateLeftTracksCurrentVelocity = 0
					stateTracksRight = 0
					stateTurretHoriz = 0
					stateTurretVert = 0
					stateHullIndicatorLeft = False
					stateHullIndicatorRight = False
					stateBBGunFiring = False
					stateTurretLights = False
					stateCameraIR = False

					printToLog(windowLog, 'All movement stopped and modules offline')
					printToLog(windowLog, 'Are you sure you want to quit? (y/n)')
					stdscr.nodelay(False) # Set getch() and getkey() to blocking
					key = stdscr.getch()
					stdscr.refresh()
					if key == ord('y'):
						mainLoop = False # The 'break' in the line below will exit the loop, but setting this variable is a backup
						stdscr.nodelay(True) # set getch() and getkey() to non-blocking
						break # Exit the loop
					else: #if not exiting the loop...
						stdscr.nodelay(True) # set getch() and getkey() back to non-blocking
						trackAccelerationLastSet = time.time() # Set trackAccelerationLastSet to current Unix time
				elif key == 263: # Backspace key - abort all movement + modules. Set pins to their default state
					printToLog(windowLog, 'All movement stopped and modules offline')

					arduinoSetupPinsState() # Set all pins to their defaults
					arduinoSetupPinsMode()
					rpiGpioSetupPinsState()
					rpiGpioSetupPinsMode()

					stateTracksLeft = 0 # Set state variables to their non-functional values
					stateLeftTracksCurrentVelocity = 0
					stateTracksRight = 0
					stateTurretHoriz = 0
					stateTurretVert = 0
					stateHullIndicatorLeft = False
					stateHullIndicatorRight = False
					stateBBGunFiring = False
					stateTurretLights = False
					stateCameraIR = False

				elif key == 32: # Space bar - fire BB gun
					stateBBGunFiring = True
				elif key == ord('q'): # Q - Turn left. Right track forward
					if stateTracksRight == 1:
						stateTracksRight = 0
					else:
						stateTracksRight = 1
				elif key == ord('a'): # A - Turn left. Left track backward
					if stateTracksLeft == -1:
						stateTracksLeft = 0
					else:
						stateTracksLeft = -1
				elif key == ord('e'): # E - Both tracks forward
					if stateTracksLeft == 1 and stateTracksRight == 1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = 1
						stateTracksRight = 1
				elif key == ord('s'): # S - Hard turn left. Left track backwards. Right track forwards
					if stateTracksLeft == -1 and stateTracksRight == 1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = -1
						stateTracksRight = 1
				elif key == ord('d'): # D - Both tracks backward
					if stateTracksLeft == -1 and stateTracksRight == -1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = -1
						stateTracksRight = -1
				elif key == ord('f'): # F - Hard Turn right. Right track forwards. Left track backwards
					if stateTracksLeft == 1 and stateTracksRight == -1:
						stateTracksLeft = 0
						stateTracksRight = 0
					else:
						stateTracksLeft = 1
						stateTracksRight = -1
				elif key == ord('t'): # T - Turn right. Left track forward
					if stateTracksLeft == 1:
						stateTracksLeft = 0
					else:
						stateTracksLeft = 1
				elif key == ord('g'): # G - Turn right. Right track backward
					if stateTracksRight == -1:
						stateTracksRight = 0
					else:
						stateTracksRight = -1
				elif key == ord('i'): # I - Turret up
					if stateTurretVert == 1:
						stateTurretVert = 0
					else:
						stateTurretVert = 1
				elif key == ord('j'): # J - Turret left
					if stateTurretHoriz == -1:
						stateTurretHoriz = 0
					else:
						stateTurretHoriz = -1
				elif key == ord('k'): # K - Turret down
					if stateTurretVert == -1:
						stateTurretVert = 0
					else:
						stateTurretVert = -1
				elif key == ord('l'): # L - Turret right
					if stateTurretHoriz == 1:
						stateTurretHoriz = 0
					else:
						stateTurretHoriz = 1
				elif key == ord('1'): # 1 - Set tracks to slowest top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_1_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_1_PWM
					printToLog(windowLog, 'Speed changed to 1')
				elif key == ord('2'): # 2 - Set tracks to medium top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_2_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_2_PWM
					printToLog(windowLog, 'Speed changed to 2')
				elif key == ord('3'): # 3 - Set tracks to fastest top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_3_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_3_PWM
					printToLog(windowLog, 'Speed changed to 3')
				elif key == ord('4'): # 4 - Set tracks to slowest acceleration
					stateTracksAcceleration = 1
					printToLog(windowLog, 'Acceleration changed to 1')
				elif key == ord('5'): # 5 - Set tracks to fastest acceleration
					stateTracksAcceleration = 2
					printToLog(windowLog, 'Acceleration changed to 2')
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
		arduinoResetPins()
		rpiGpioResetPins()
		print('Exception')
		print(e)
	except KeyboardInterrupt as e:
		arduinoResetPins()
		rpiGpioResetPins()
		print('KeyboardInterrupt')
		print(e)
	except:
		arduinoResetPins()
		rpiGpioResetPins()

	arduinoResetPins()
	rpiGpioResetPins()
