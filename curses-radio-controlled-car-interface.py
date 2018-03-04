#!/usr/bin/python3

##############
## SETTINGS ##
##############

# Debug settings
DEBUG_VERBOSE_MODE    = True
FAKE_AN_ARDUINO       = True
FAKE_RASPBERRYPI_GPIO = True

# Nanpy settings
SERIAL_PORT = '/dev/serial0'

# Key states
KEY_Q = False
KEY_A = False
KEY_E = False
KEY_S = False
KEY_D = False
KEY_F = False
KEY_T = False
KEY_G = False

KEY_I = False
KEY_J = False
KEY_K = False
KEY_L = False

KEY_1 = False
KEY_2 = False
KEY_3 = False
KEY_4 = False
KEY_5 = False
KEY_6 = False
KEY_7 = False
KEY_8 = False
KEY_9 = False
KEY_0 = False

KEY_ESCAPE    = False
KEY_ENTER     = False
KEY_BACKSPACE = False
KEY_SPACE     = False

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

cursesWindowMinimumX = 126
cursesWindowMinimumY = 29
logY = 3
logTotal = 1


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
	printToLogDebug('trackLeftForward')
	aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.HIGH)
	aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
	aa.analogWrite(TRACK_LEFT_PWM_PIN, speed)
def trackLeftBackward(speed):
	printToLogDebug('trackLeftBackward')
	aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
	aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.HIGH)
	aa.analogWrite(TRACK_LEFT_PWM_PIN, speed)
def trackLeftStop():
	printToLogDebug('trackLeftStop')
	aa.digitalWrite(TRACK_LEFT_FORWARD_PIN, aa.LOW)
	aa.digitalWrite(TRACK_LEFT_BACKWARD_PIN, aa.LOW)
	aa.analogWrite(TRACK_LEFT_PWM_PIN, 0)

def trackRightForward(speed):
	printToLogDebug('trackRightForward')
	aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.HIGH)
	aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
	aa.analogWrite(TRACK_RIGHT_PWM_PIN, speed)

def trackRightBackward(speed):
	printToLogDebug('trackRightBackward')
	aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
	aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.HIGH)
	aa.analogWrite(TRACK_RIGHT_PWM_PIN, speed)

def trackRightStop():
	printToLogDebug('trackRightStop')
	aa.digitalWrite(TRACK_RIGHT_FORWARD_PIN, aa.LOW)
	aa.digitalWrite(TRACK_RIGHT_BACKWARD_PIN, aa.LOW)
	aa.analogWrite(TRACK_RIGHT_PWM_PIN, 0)

def turretLeft(speed):
	printToLogDebug('turretLeft')
	aa.digitalWrite(TURRET_LEFT_PIN, aa.HIGH)
	aa.digitalWrite(TURRET_RIGHT_PIN, aa.LOW)
	aa.analogWrite(TURRET_X_PWM_PIN, speed)
def turretRight(speed):
	printToLogDebug('turretRight')
	aa.digitalWrite(TURRET_LEFT_PIN, aa.LOW)
	aa.digitalWrite(TURRET_RIGHT_PIN, aa.HIGH)
	aa.analogWrite(TURRET_X_PWM_PIN, speed)
def turretXStop():
	printToLogDebug('turretXStop')
	aa.digitalWrite(TURRET_LEFT_PIN, aa.LOW)
	aa.digitalWrite(TURRET_RIGHT_PIN, aa.LOW)
	aa.analogWrite(TURRET_X_PWM_PIN, 0)

def turretUp(speed):
	printToLogDebug('turretUp')
	aa.digitalWrite(TURRET_UP_PIN, aa.HIGH)
	aa.digitalWrite(TURRET_DOWN_PIN, aa.LOW)
def turretDown(speed):
	printToLogDebug('turretDown')
	aa.digitalWrite(TURRET_UP_PIN, aa.LOW)
	aa.digitalWrite(TURRET_DOWN_PIN, aa.HIGH)
def turretYStop():
	printToLogDebug('turretYStop')
	aa.digitalWrite(TURRET_UP_PIN, aa.LOW)
	aa.digitalWrite(TURRET_DOWN_PIN, aa.LOW)

def fireGun():
	printToLogDebug('Firing gun not implemented')

def arduinoSetupPins():
	printToLogDebug('Setting up pins')
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

def arduinoUnsetPins():
	printToLogDebug("Setting pins to input, low")
	for i in range(1,20):
		aa.digitalWrite(i, aa.LOW)
		aa.pinMode(i, aa.INPUT)
		time.sleep(0.05)


#################################
## RASPBERRY PI GPIO FUNCTIONS ##
#################################

#WIP


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
	if y >= cursesWindowMinimumY and x >= cursesWindowMinimumX:
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

def printButtonInformation(windowButtonInformation):
	windowButtonInformation.addstr(1,1, 'Information')

	curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

	printButton(windowButtonInformation, 2, 2,  'Q', KEY_Q)
	printButton(windowButtonInformation, 6, 2,  'A', KEY_A)

	printButton(windowButtonInformation, 2, 10, 'E', KEY_E)
	printButton(windowButtonInformation, 6, 6,  'S', KEY_S)
	printButton(windowButtonInformation, 6, 10, 'D', KEY_D)
	printButton(windowButtonInformation, 6, 14, 'F', KEY_F)

	printButton(windowButtonInformation, 2, 18, 'T', KEY_T)
	printButton(windowButtonInformation, 6, 18, 'G', KEY_G)

	printButton(windowButtonInformation, 2, 30, 'I', KEY_I)
	printButton(windowButtonInformation, 6, 26, 'J', KEY_J)
	printButton(windowButtonInformation, 6, 30, 'K', KEY_K)
	printButton(windowButtonInformation, 6, 34, 'L', KEY_L)
	
	printButton(windowButtonInformation, 2, 46, '1', KEY_1)
	printButton(windowButtonInformation, 2, 50, '2', KEY_2)
	printButton(windowButtonInformation, 2, 54, '3', KEY_3)
	printButton(windowButtonInformation, 2, 58, '4', KEY_4)
	printButton(windowButtonInformation, 2, 62, '5', KEY_5)

	printButton(windowButtonInformation, 6, 46, '6', KEY_6)
	printButton(windowButtonInformation, 6, 50, '7', KEY_7)
	printButton(windowButtonInformation, 6, 54, '8', KEY_8)
	printButton(windowButtonInformation, 6, 58, '9', KEY_9)
	printButton(windowButtonInformation, 6, 62, '0', KEY_0)
	
	printButton(windowButtonInformation, 2, 74, 'Escape',    KEY_ESCAPE)
	printButton(windowButtonInformation, 6, 74, 'Enter',     KEY_ENTER)
	printButton(windowButtonInformation, 2, 83, 'Backspace', KEY_BACKSPACE)
	printButton(windowButtonInformation, 6, 83, 'Space',     KEY_SPACE)

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
		printButtonInformation(windowButtonInformation)

		stdscr.refresh()

		printToLog(windowLog, 'Curses started')
		printToLogDebug(windowLog, 'Terminal size: ' + str(x) + 'x' + str(y))
		printTankBatteryLevels(windowTankModules, 8.4, 3.2, 7.4) # Testing
		

		if not FAKE_AN_ARDUINO:
			connection = nanpy.SerialManager(device=SERIAL_PORT)
			aa = nanpy.ArduinoApi(connection=connection)
			at = nanpy.arduinotree.ArduinoTree(connection=connection)
		
		time.sleep(5)
	else:
		endCurses()
		print('Curses window is too small')
		print('Minimum size is ' + str(cursesWindowMinimumX) + ' rows by ' + str(cursesWindowMinimumY) + ' lines')
		print('Current size is ' + str(stdscr.getmaxyx()[1]) + ' rows by ' + str(stdscr.getmaxyx()[0]) + ' lines')

	time.sleep(5)

if __name__ == "__main__":
	try:
		curses.wrapper(main_curses)
	except RuntimeError as e:
		print(e)
