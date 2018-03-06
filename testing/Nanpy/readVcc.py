#!/usr/bin/python3
import time, nanpy, nanpy.arduinotree, nanpy.register, nanpy.vcc

connection = nanpy.SerialManager(device='/dev/serial0')
aa = nanpy.ArduinoApi(connection=connection)
at = nanpy.arduinotree.ArduinoTree(connection=connection)

def test_vcc1():
	print("1 " + str(at.vcc.read()))

def test_vcc2():
	vcc = nanpy.vcc.Vcc(nanpy.register.RegisterFeature())
	print("2 " + str(vcc.read()))

def test_vcc3():
	print("3 " + str(nanpy.vcc.Vcc(nanpy.register.RegisterFeature()).read()))

def test_vcc4():
	x = at.vcc.read()
	print('4 %.4f V' % x)


test_vcc1()
test_vcc2()
test_vcc3()
test_vcc4()
