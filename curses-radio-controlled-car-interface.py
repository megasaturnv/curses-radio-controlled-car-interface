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

TRACK_LEFT_TWEAK_VELOCITY_AMOUNT = 10
TRACK_RIGHT_TWEAK_VELOCITY_AMOUNT = 10

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
RPI_UART_DTR              = 17


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
		aa.digitalWrite(BBGUN_FIRE_READY_PIN, aa.LOW)
		aa.digitalWrite(TURRET_LIGHTS_PIN, aa.HIGH)
		aa.digitalWrite(CAMERA_IR_CONTROL_PIN, aa.LOW)
		aa.digitalWrite(BATTERY_VOLTAGE_LIION_RPI_PIN, aa.LOW) #A6
		aa.digitalWrite(BATTERY_VOLTAGE_LIION_1X3_PIN, aa.LOW) #A3
		aa.digitalWrite(BATTERY_VOLTAGE_LIION_2X3_PIN, aa.LOW) #A7

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
		#aa.pinMode(BBGUN_FIRE_READY_PIN, aa.OUTPUT)
		aa.pinMode(TURRET_LIGHTS_PIN, aa.OUTPUT)
		#aa.pinMode(CAMERA_IR_CONTROL_PIN, aa.OUTPUT)
		aa.pinMode(BATTERY_VOLTAGE_LIION_RPI_PIN, aa.INPUT) #A6
		aa.pinMode(BATTERY_VOLTAGE_LIION_1X3_PIN, aa.INPUT) #A3
		aa.pinMode(BATTERY_VOLTAGE_LIION_2X3_PIN, aa.INPUT) #A7

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
			aa.pinMode(i, aa.INPUT)
			aa.digitalWrite(i, aa.LOW)
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

def rpiResetArduino(): # Reset Arduino by pulsing RPI_UART_DTR pin
	if not FAKE_RASPBERRYPI_GPIO:
		pass

# Not yet implemented. Work in progress


######################
## CURSES FUNCTIONS ##
######################

def endCurses(stdscr):
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
	global stateLeftTracksTargetSpeed, stateRightTracksTargetSpeed, stateTracksAcceleration # Global variables - Vehicle states
	if not FAKE_AN_ARDUINO: # Global variables - Nanpy
		global aa, at

	# Local variables
	stateHullIndicatorLeft          = False
	stateHullIndicatorLeftModified  = True
	stateHullIndicatorRight         = False
	stateHullIndicatorRightModified = True
	stateTurretLights               = False
	stateTurretLightsModified       = True
	stateCameraIR                   = False
	stateCameraIRModified           = True
	stateBBGunFiring                = False

	# Current state of tracks and turret motors
	# 'ba' = Backwards (Accelerating or decelerating. Activates acceleration calculation)
	# 'fa' = Forwards (Accelerating or decelerating. Activates acceleration calculation)
	# 'sm' = Stop motor (Tank moving but slowly stopping. Activates acceleration calculation)
	# 'sc' = Speed change (Used for tweaking track's speed while moving)
	# 'nc' = No change. No commands sent to Arduino. Motor controller will remain in current state (direction + speed)
	stateTracksLeft  = 'sm'
	stateTracksRight = 'sm'
	stateTurretHoriz = 'sm'
	stateTurretVert  = 'sm'
	trackLeftCurrentVelocity  = 0 # Current velocity of tracks between -255 and 255. Positive/Negative represents direction. Absolute number represents speed as PWM value.
	trackRightCurrentVelocity = 0 # Current velocity of tracks between -255 and 255. Positive/Negative represents direction. Absolute number represents speed as PWM value.
	trackAccelerationLastSet = time.time()

	# Curses settings
	#stdscr = curses.initscr() # setup initial window
	#curses.start_color() # Enable curses colour
	#curses.use_default_colors() # Use default curses colours
	curses.noecho()        # Don't echo keystrokes
	curses.cbreak()        # Don't wait for enter, handle keys immediately
	stdscr.keypad(True)    # Use aliases for special keys
	curses.curs_set(False) # Suppress the blinking cursor
	stdscr.nodelay(True)   # Set getch() and getkey() to non-blocking

	# Setup Arduino connection
	if not FAKE_AN_ARDUINO:
		connection = nanpy.SerialManager(device=SERIAL_PORT)
		aa = nanpy.ArduinoApi(connection=connection)
		at = nanpy.arduinotree.ArduinoTree(connection=connection)

	y, x = stdscr.getmaxyx()
	if checkCursesWindowSize(stdscr):
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
				if stateTracksLeft == 'fa': # If track is accelerating forward
					if abs(trackLeftCurrentVelocity) <= stateLeftTracksTargetSpeed: # If current speed is smaller than or equal to target speed
						trackLeftCurrentVelocity += min(abs(stateLeftTracksTargetSpeed - trackLeftCurrentVelocity), int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Increase current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
					else: # Else (if current speed is larger than the target speed)
						trackLeftCurrentVelocity -= min(abs(stateLeftTracksTargetSpeed - trackLeftCurrentVelocity), int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Decrease current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
				elif stateTracksLeft == 'ba': # If track is accelerating backward
					if abs(trackLeftCurrentVelocity) <= stateLeftTracksTargetSpeed: # If current speed is smaller than or equal to target speed
						trackLeftCurrentVelocity -= min(abs(-stateLeftTracksTargetSpeed - trackLeftCurrentVelocity), int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Decrease current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
					else: # Else (if current speed is larger than the target speed)
						trackLeftCurrentVelocity += min(abs(-stateLeftTracksTargetSpeed - trackLeftCurrentVelocity), int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Increase current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
				elif stateTracksLeft == 'sm': # If track is stopping / stopped
					if trackLeftCurrentVelocity > 0: # If trackLeftCurrentVelocity is positive
						trackLeftCurrentVelocity -= int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime from trackLeftCurrentVelocity
						if trackLeftCurrentVelocity < 0: # If above calculation set trackLeftCurrentVelocity to a negative value...
							trackLeftCurrentVelocity = 0 # Set trackLeftCurrentVelocity to 0
					elif trackLeftCurrentVelocity < 0: # If trackLeftCurrentVelocity is negative
						trackLeftCurrentVelocity += int(TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime to trackLeftCurrentVelocity
						if trackLeftCurrentVelocity > 0: # If above calculation set trackLeftCurrentVelocity to a negative value...
							trackLeftCurrentVelocity = 0 # Set trackLeftCurrentVelocity to 0

				# Velocity and acceleration calculation code - Right track
				if stateTracksRight == 'fa': # If track is accelerating forward
					if abs(trackRightCurrentVelocity) <= stateRightTracksTargetSpeed: # If current speed is smaller than or equal to target speed
						trackRightCurrentVelocity += min(abs(stateRightTracksTargetSpeed - trackRightCurrentVelocity), int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Increase current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
					else: # Else (if current speed is larger than the target speed)
						trackRightCurrentVelocity -= min(abs(stateRightTracksTargetSpeed - trackRightCurrentVelocity), int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Decrease current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
				elif stateTracksRight == 'ba': # If track is accelerating backward
					if abs(trackRightCurrentVelocity) <= stateRightTracksTargetSpeed: # If current speed is smaller than or equal to target speed
						trackRightCurrentVelocity -= min(abs(-stateRightTracksTargetSpeed - trackRightCurrentVelocity), int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Decrease current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
					else: # Else (if current speed is larger than the target speed)
						trackRightCurrentVelocity += min(abs(-stateRightTracksTargetSpeed - trackRightCurrentVelocity), int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime)) # Increase current velocity until the speed change to the target speed is a larger number than TRACK_LEFT_SLOW_ACCELERATION_FACTOR * elapsedTime
				elif stateTracksRight == 'sm': # If track is stopping / stopped
					if trackRightCurrentVelocity > 0: # If trackRightCurrentVelocity is positive
						trackRightCurrentVelocity -= int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Subtract TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime from trackRightCurrentVelocity
						if trackRightCurrentVelocity < 0: # If above calculation set trackRightCurrentVelocity to a negative value...
							trackRightCurrentVelocity = 0 # Set trackRightCurrentVelocity to 0
					elif trackRightCurrentVelocity < 0: # If trackRightCurrentVelocity is negative
						trackRightCurrentVelocity += int(TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime) # Add TRACK_RIGHT_SLOW_ACCELERATION_FACTOR * elapsedTime to trackRightCurrentVelocity
						if trackRightCurrentVelocity > 0: # If above calculation set trackRightCurrentVelocity to a negative value...
							trackRightCurrentVelocity = 0 # Set trackRightCurrentVelocity to 0

			elif stateTracksAcceleration == 2: # If stateTracksAcceleration == 2...
				# Left tracks
				if stateTracksLeft == 'fa': # If track is accelerating forward...
					trackLeftCurrentVelocity = stateLeftTracksTargetSpeed # Set current velocity to positive target speed instantly
				if stateTracksLeft == 'ba': # If track is accelerating backward...
					trackLeftCurrentVelocity = -stateLeftTracksTargetSpeed # Set current velocity to negative target speed instantly
				elif stateTracksLeft == 'sm': # If track is stopping / stopped...
					trackLeftCurrentVelocity = 0 # Set current velocity to 0 instantly
				# Check if left tracks are going too fast
				if trackLeftCurrentVelocity > stateLeftTracksTargetSpeed: # If current velocity is larger than target speed
					trackLeftCurrentVelocity = stateLeftTracksTargetSpeed # Set current velocity to positive target speed
				if trackLeftCurrentVelocity < -stateLeftTracksTargetSpeed: # If current velocity is smaller than negative target speed
					trackLeftCurrentVelocity = -stateLeftTracksTargetSpeed # Set current velocity to negative target speed

				# Right tracks
				if stateTracksRight == 'fa': # If track is accelerating forward...
					trackRightCurrentVelocity = stateRightTracksTargetSpeed # Set current velocity to positive target speed instantly
				if stateTracksRight == 'ba': # If track is accelerating backward...
					trackRightCurrentVelocity = -stateRightTracksTargetSpeed # Set current velocity to negative target speed instantly
				elif stateTracksRight == 'sm': # If track is stopping / stopped...
					trackRightCurrentVelocity = 0 # Set current velocity to 0 instantly
				# Check if right tracks are going too fast
				if trackRightCurrentVelocity > stateRightTracksTargetSpeed: # If current velocity is larger than target speed
					trackRightCurrentVelocity = stateRightTracksTargetSpeed # Set current velocity to positive target speed
				if trackRightCurrentVelocity < -stateRightTracksTargetSpeed: # If current velocity is smaller than negative target speed
					trackRightCurrentVelocity = -stateRightTracksTargetSpeed # Set current velocity to negative target speed

			trackAccelerationLastSet = time.time() # Set trackAccelerationLastSet to current Unix time


			# Vehicle states checking code - tracks
			if stateTracksLeft == 'sc':
				printToLogDebug(windowLog, 'Left track speed set to abs of: ' + str(trackLeftCurrentVelocity))
				trackLeftSpeed(abs(trackLeftCurrentVelocity)) # Set left track speed
			elif stateTracksLeft == 'ba' or stateTracksLeft == 'fa':
				printToLogDebug(windowLog, 'Left track velocity set to: ' + str(trackLeftCurrentVelocity))
				trackLeft(trackLeftCurrentVelocity) # Set left track motion
			elif stateTracksLeft == 'sm':
				if trackLeftCurrentVelocity == 0:
					trackLeft(0) # Stop all left track motion
					printToLogDebug(windowLog, 'Left track stopped. Velocity: ' + str(trackLeftCurrentVelocity))
				else:
					trackLeftSpeed(abs(trackLeftCurrentVelocity)) # Set left track PWM speed to trackLeftCurrentVelocity
					printToLogDebug(windowLog, 'Left track stopping. Velocity: ' + str(trackLeftCurrentVelocity))

			if stateTracksRight == 'sc':
				printToLogDebug(windowLog, 'Right track speed set to abs of: ' + str(trackRightCurrentVelocity))
				trackRightSpeed(abs(trackRightCurrentVelocity)) # Set right track speed
			elif stateTracksRight == 'ba' or stateTracksRight == 'fa':
				printToLogDebug(windowLog, 'Right track velocity set to: ' + str(trackRightCurrentVelocity))
				trackRight(trackRightCurrentVelocity) # Set right track motion
			elif stateTracksRight == 'sm':
				if trackRightCurrentVelocity == 0:
					trackRight(0) # Stop all right track motion
					printToLogDebug(windowLog, 'Right track stopped. Velocity: ' + str(trackRightCurrentVelocity))
				else:
					trackRightSpeed(abs(trackRightCurrentVelocity)) # Set right track PWM speed to trackRightCurrentVelocity
					printToLogDebug(windowLog, 'Right track stopping. Velocity: ' + str(trackRightCurrentVelocity))


			# Vehicle tracks target speed checking code. This will set their states to 'nc' if target speed has been reached
			if stateTracksLeft == 'sc' or abs(trackLeftCurrentVelocity) == stateLeftTracksTargetSpeed or (trackLeftCurrentVelocity == 0 and stateTracksLeft == 'sm'): # Tracks have stopped or reached top speed - set stateTracksLeft to 'nc'
				stateTracksLeft = 'nc'
			if stateTracksRight == 'sc' or abs(trackRightCurrentVelocity) == stateRightTracksTargetSpeed or (trackRightCurrentVelocity == 0 and stateTracksRight == 'sm'): # Tracks have stopped or reached top speed - set stateTracksRight to 'nc'
				stateTracksRight = 'nc'


			# Vehicle states checking code - turret
			if stateTurretHoriz == 'ba':
				printToLogDebug(windowLog, 'Turret horiz left')
				turretLeft(TURRET_LEFT_SPEED_PWM) # Set turret horizontal motion
			elif stateTurretHoriz == 'sm':
				printToLogDebug(windowLog, 'Turret horiz stopped')
				turretXStop() # Stop all horizontal turret motion
				stateTurretHoriz = 'nc'
			elif stateTurretHoriz == 'fa':
				printToLogDebug(windowLog, 'Turret horiz right')
				turretRight(TURRET_RIGHT_SPEED_PWM) # Set turret horizontal motion

			if stateTurretVert == 'ba':
				printToLogDebug(windowLog, 'Turret vert down')
				turretDown(TURRET_DOWN_SPEED_PWM) # Set turret vertical motion
			elif stateTurretVert == 'sm':
				printToLogDebug(windowLog, 'Turret vert stopped')
				turretYStop() # Stop all vertical turret motion
				stateTurretVert = 'nc'
			elif stateTurretVert == 'fa':
				printToLogDebug(windowLog, 'Turret vert up')
				turretUp(TURRET_UP_SPEED_PWM) # Set turret vertical motion

			# Vehicle states checking code - modules
			if stateHullIndicatorLeftModified:
				stateHullIndicatorLeftModified = False
			if stateHullIndicatorRightModified:
				stateHullIndicatorRightModified = False
			if stateTurretLightsModified:
				if stateTurretLights: # Turn turret lights on
					printToLogDebug(windowLog, 'Turning turret lights on')
					if not FAKE_AN_ARDUINO:
						aa.digitalWrite(TURRET_LIGHTS_PIN, aa.LOW) # Pull PNP transistor base low to enable current flow and turn on turret lights
				else:
					printToLogDebug(windowLog, 'Turning turret lights off')
					if not FAKE_AN_ARDUINO:
						aa.digitalWrite(TURRET_LIGHTS_PIN, aa.HIGH) # Set PNP transistor base to high to stop current flow and turn off turret lights
				stateTurretLightsModified = False
			if stateCameraIRModified:
				stateCameraIRModified = False
			if stateBBGunFiring:
				#fireBBGun()
				stateBBGunFiring = False


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

					trackLeftCurrentVelocity = 0
					trackRightCurrentVelocity = 0
					stateTracksLeft = 'sm' # Set state variables to their non-functional values
					stateTracksRight = 'sm'
					stateTurretHoriz = 'sm'
					stateTurretVert = 'sm'
					stateHullIndicatorLeft          = False
					stateHullIndicatorLeftModified  = True
					stateHullIndicatorRight         = False
					stateHullIndicatorRightModified = True
					stateBBGunFiring                = False
					stateBBGunFiringModified        = True
					stateTurretLights               = False
					stateTurretLightsModified       = True
					stateCameraIR                   = False

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

					trackLeftCurrentVelocity = 0
					trackRightCurrentVelocity = 0
					stateTracksLeft = 'sm' # Set state variables to their non-functional values
					stateTracksRight = 'sm'
					stateTurretHoriz = 'sm'
					stateTurretVert = 'sm'
					stateHullIndicatorLeft          = False
					stateHullIndicatorLeftModified  = True
					stateHullIndicatorRight         = False
					stateHullIndicatorRightModified = True
					stateBBGunFiring                = False
					stateBBGunFiringModified        = True
					stateTurretLights               = False
					stateTurretLightsModified       = True
					stateCameraIR                   = False

				elif key == 32: # Space bar - fire BB gun
					stateBBGunFiring = True
				# ESDF keys
				elif key == ord('e'): # E - Both tracks forward
					if trackLeftCurrentVelocity > 0 and trackRightCurrentVelocity > 0:
						stateTracksLeft = 'sm'
						stateTracksRight = 'sm'
					else:
						stateTracksLeft = 'fa'
						stateTracksRight = 'fa'
				elif key == ord('s'): # S - Hard turn left. Left track backwards. Right track forwards
					if trackLeftCurrentVelocity < 0 and trackRightCurrentVelocity > 0:
						stateTracksLeft = 'sm'
						stateTracksRight = 'sm'
					else:
						stateTracksLeft = 'ba'
						stateTracksRight = 'fa'
				elif key == ord('d'): # D - Both tracks backward
					if trackLeftCurrentVelocity < 0 and trackRightCurrentVelocity < 0:
						stateTracksLeft = 'sm'
						stateTracksRight = 'sm'
					else:
						stateTracksLeft = 'ba'
						stateTracksRight = 'ba'
				elif key == ord('f'): # F - Hard Turn right. Right track forwards. Left track backwards
					if trackLeftCurrentVelocity > 0 and trackRightCurrentVelocity < 0:
						stateTracksLeft = 'sm'
						stateTracksRight = 'sm'
					else:
						stateTracksLeft = 'fa'
						stateTracksRight = 'ba'
				# WXRV keys
				elif key == ord('w'): # W - Slightly increase velocity of left track. Track will not go faster than stateLeftTracksTargetSpeed
					trackLeftCurrentVelocity += TRACK_LEFT_TWEAK_VELOCITY_AMOUNT
					stateTracksLeft = 'sc'
				elif key == ord('x'): # X - Slightly decrease velocity of left track.
					trackLeftCurrentVelocity -= TRACK_LEFT_TWEAK_VELOCITY_AMOUNT
					stateTracksLeft = 'sc'
				elif key == ord('r'): # R - Slightly increase velocity of right track. Track will not go faster than stateLeftTracksTargetSpeed
					trackRightCurrentVelocity += TRACK_RIGHT_TWEAK_VELOCITY_AMOUNT
					stateTracksRight = 'sc'
				elif key == ord('v'): # V - Slightly decrease velocity of right track.
					trackRightCurrentVelocity -= TRACK_RIGHT_TWEAK_VELOCITY_AMOUNT
					stateTracksRight = 'sc'

				#QATG keys
				elif key == ord('q'): # Q - Left track forward
					if trackLeftCurrentVelocity > 0:
						stateTracksLeft = 'sm'
					else:
						stateTracksLeft = 'fa'
				elif key == ord('a'): # A - Left track backward
					if trackLeftCurrentVelocity < 0:
						stateTracksLeft = 'sm'
					else:
						stateTracksLeft = 'ba'
				elif key == ord('t'): # T - Right track forward
					if trackRightCurrentVelocity > 0:
						stateTracksRight = 'sm'
					else:
						stateTracksRight = 'fa'
				elif key == ord('g'): # G - Right track backward
					if trackRightCurrentVelocity < 0:
						stateTracksRight = 'sm'
					else:
						stateTracksRight = 'ba'

				#IJKL keys
				elif key == ord('i'): # I - Turret up
					if stateTurretVert == 'fa':
						stateTurretVert = 'sm'
					else:
						stateTurretVert = 'fa'
				elif key == ord('j'): # J - Turret left
					if stateTurretHoriz == 'ba':
						stateTurretHoriz = 'sm'
					else:
						stateTurretHoriz = 'ba'
				elif key == ord('k'): # K - Turret down
					if stateTurretVert == 'ba':
						stateTurretVert = 'sm'
					else:
						stateTurretVert = 'ba'
				elif key == ord('l'): # L - Turret right
					if stateTurretHoriz == 'fa':
						stateTurretHoriz = 'sm'
					else:
						stateTurretHoriz = 'fa'
				elif key == ord('1'): # 1 - Set tracks to slowest top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_1_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_1_PWM
					# Could just set stateTracksLeft = 'sc' etc below. But this would not accelerate tracks when changing to a higher speed value
					if trackLeftCurrentVelocity > 0: # If tank track is moving forward
						stateTracksLeft = 'fa' # Start accelerating track forwards to new target speed
					elif trackLeftCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksLeft = 'ba' # Start accelerating track backwards to new target speed
					if trackRightCurrentVelocity > 0: # If tank track is moving forward
						stateTracksRight = 'fa' # Start accelerating track forwards to new target speed
					elif trackRightCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksRight = 'ba' # Start accelerating track backwards to new target speed
					printToLog(windowLog, 'Speed changed to 1')
				elif key == ord('2'): # 2 - Set tracks to medium top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_2_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_2_PWM
					if trackLeftCurrentVelocity > 0: # If tank track is moving forward
						stateTracksLeft = 'fa' # Start accelerating track forwards to new target speed
					elif trackLeftCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksLeft = 'ba' # Start accelerating track backwards to new target speed
					if trackRightCurrentVelocity > 0: # If tank track is moving forward
						stateTracksRight = 'fa' # Start accelerating track forwards to new target speed
					elif trackRightCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksRight = 'ba' # Start accelerating track backwards to new target speed
					printToLog(windowLog, 'Speed changed to 2')
				elif key == ord('3'): # 3 - Set tracks to fastest top speed
					stateLeftTracksTargetSpeed = TRACK_LEFT_SPEED_3_PWM
					stateRightTracksTargetSpeed = TRACK_RIGHT_SPEED_3_PWM
					if trackLeftCurrentVelocity > 0: # If tank track is moving forward
						stateTracksLeft = 'fa' # Start accelerating track forwards to new target speed
					elif trackLeftCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksLeft = 'ba' # Start accelerating track backwards to new target speed
					if trackRightCurrentVelocity > 0: # If tank track is moving forward
						stateTracksRight = 'fa' # Start accelerating track forwards to new target speed
					elif trackRightCurrentVelocity < 0: # Else if tank track is moving backward...
						stateTracksRight = 'ba' # Start accelerating track backwards to new target speed
					printToLog(windowLog, 'Speed changed to 3')
				elif key == ord('4'): # 4 - Set tracks to slowest acceleration
					stateTracksAcceleration = 1
					printToLog(windowLog, 'Acceleration changed to 1')
				elif key == ord('5'): # 5 - Set tracks to fastest acceleration
					stateTracksAcceleration = 2
					printToLog(windowLog, 'Acceleration changed to 2')
				elif key == ord('6'): # 6 - Toggle left indicator LED
					printToLog(windowLog, 'Left indicator')
				elif key == ord('7'): # 7 - Toggle right indicator LED
					printToLog(windowLog, 'Right indicator')
				elif key == ord('8'): # 8 - Toggle turret LEDs
					stateTurretLights = not stateTurretLights
					stateTurretLightsModified = True
					printToLog(windowLog, 'Toggled turret LEDs to: ' + str(stateTurretLights))
				elif key == ord('9'): # 9 - Toggle IR LEDs
					printToLog(windowLog, 'IR LEDs')
				elif key == ord('0'): # 0 - Fire BB gun
					printToLog(windowLog, 'BB gun')
				else:
					printToLog(windowLog, 'Warning: Pressed key not recognised: ' + chr(key) + ' = ' + str(key))

			#else:
				#printToLogDebug(windowLog, 'No key pressed')

			key = -1
	else:
		endCurses(stdscr)
		print('Curses window is too small')
		print('Minimum size is ' + str(CURSES_WINDOW_MIN_X) + ' rows by ' + str(CURSES_WINDOW_MIN_Y) + ' lines')
		print('Current size is ' + str(x) + ' rows by ' + str(y) + ' lines')

if __name__ == "__main__":
#	try:
	curses.wrapper(main_curses)
#	except Exception as e:
#	#except RuntimeError as e:
#		arduinoResetPins()
#		rpiGpioResetPins()
#		print('Exception')
#		print(e)
#	except KeyboardInterrupt as e:
#		arduinoResetPins()
#		rpiGpioResetPins()
#		print('KeyboardInterrupt')
#		print(e)
#	except:
#		arduinoResetPins()
#		rpiGpioResetPins()
#
#	arduinoResetPins()
#	rpiGpioResetPins()
