# curses-radio-controlled-car-interface
A python curses program which allows the user to drive radio-controlled vehicles via Raspberry Pi GPIO pins and/or an arduino connected to the serial port with Nanpy.
In this program, the radio-controlled vehicle is a model tank. The keyboard controls and interface reflect this.

## Keyboard Controls
```
E = Both tracks forward
S = Right track forward. Left track backward
D = Both tracks backward
F = Left track forward. Right track backward

W = Increase left track velocity slightly
X = Decrease left track velocity slightly
R = Increase right track velocity slightly
V = Decrease right track velocity slightly

Q = Left track forward
A = Left track backward
T = Right track forward
G = Right track backward

I = Turret up
J = Turret left
K = Turret down
L = Turret right

1 = Set target speed to 1 (slowest)
2 = Set target speed to 2
3 = Set target speed to 3 (fastest, default)
4 = Turn on slow acceleration mode
5 = Turn off slow acceleration mode (default)

6 = Function key 6. Not implemented (Will be left indicator)
7 = Function key 7. Not implemented (Will be right indicator)
8 = Function key 8. Not implemented (Will toggle the turret LEDs)
9 = Function key 9. Not implemented (Will Toggle IR LEDs)
0 = Function key 0. Not implemented (Will fire BB gun)
```
## Libraries Used
* Python Curses
* Nanpy https://github.com/nanpy/nanpy
* RPi.GPIO https://pypi.python.org/pypi/RPi.GPIO
