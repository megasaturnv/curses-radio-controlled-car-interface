#!/usr/bin/python3
import time, nanpy

BATTERY_VOLTAGE_LIION_RPI_PIN = 20 #A6
BATTERY_VOLTAGE_LIION_1X3_PIN = 17 #A3
BATTERY_VOLTAGE_LIION_2X3_PIN = 21 #A7

connection = nanpy.SerialManager(device='/dev/serial0')

aa = nanpy.ArduinoApi(connection=connection)
aa.pinMode(BATTERY_VOLTAGE_LIION_RPI_PIN, aa.INPUT)
aa.pinMode(BATTERY_VOLTAGE_LIION_1X3_PIN, aa.INPUT)
aa.pinMode(BATTERY_VOLTAGE_LIION_2X3_PIN, aa.INPUT)

RaspberryPiLiIonCombined       = aa.analogRead(BATTERY_VOLTAGE_LIION_RPI_PIN)*0.0048875855327468 * 2
RaspberryPiLiIonAveragePerCell = RaspberryPiLiIonCombined / 2

tankModulesLiIonFirstCell  =     aa.analogRead(BATTERY_VOLTAGE_LIION_1X3_PIN)*0.0048875855327468
tankModulesLiIonCombined   =     aa.analogRead(BATTERY_VOLTAGE_LIION_2X3_PIN)*0.0048875855327468 * 2
tankModulesLiIonSecondCell =     tankModulesLiIonCombined - tankModulesLiIonFirstCell

print('A6 BATTERY_VOLTAGE_LIION_RPI_PIN  RaspberryPiLiIonCombined        7.4v nominal: ' + str(RaspberryPiLiIonCombined))
print('                                  RaspberryPiLiIonAveragePerCell  3.7v nominal: ' + str(RaspberryPiLiIonAveragePerCell))

print('A3 BATTERY_VOLTAGE_LIION_1X3_PIN  tankModulesLiIonFirstCell       3.7v nominal: ' + str(tankModulesLiIonFirstCell))
print('                                  tankModulesLiIonSecondCell      3.7v nominal: ' + str(tankModulesLiIonCombined))
print('A7 BATTERY_VOLTAGE_LIION_2X3_PIN  tankModulesLiIonCombined        7.4v nominal: ' + str(tankModulesLiIonSecondCell))
