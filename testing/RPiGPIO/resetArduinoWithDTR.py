#!/usr/bin/python

import time
import RPi.GPIO as GPIO

ARDUINO_DTR = 17

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

GPIO.setup(ARDUINO_DTR, GPIO.OUT)
GPIO.output(ARDUINO_DTR, GPIO.HIGH)
time.sleep(0.12)
GPIO.output(ARDUINO_DTR, GPIO.LOW)
time.sleep(0.12)
GPIO.output(ARDUINO_DTR, GPIO.HIGH)
print("Arduino reset via DTR pin on GPIO pin: " + str(ARDUINO_DTR))

GPIO.cleanup()
print("GPIO cleaned up")
