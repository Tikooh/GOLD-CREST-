
[![Website](https://img.shields.io/badge/Website-Link-blue.svg)](https://gavinlyonsrepo.github.io/)  [![Rss](https://img.shields.io/badge/Subscribe-RSS-yellow.svg)](https://gavinlyonsrepo.github.io//feed.xml)  [![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/paypalme/whitelight976)

# RpiMotorLib,


![ScreenShot dcmotor](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/RF310T11400.jpg)
![ScreenShot Nema](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/nema11.jpg)
![ScreenShot L298N](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/L298N.jpg)
![ScreenShot A4988](https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/images/A4988.jpg)

Table of contents
---------------------------

  * [Table of contents](#table-of-contents)
  * [Overview](#overview)
  * [Installation](#installation)
  * [Hardware](#hardware)
  * [Software](#software)
  * [Notes](#notes-and-issues)

Overview
--------------------------------------------
* Name: RpiMotorLib
* Title: Raspberry pi motor library.
* Description: 

A python 3 library to drive motor controllers and servos with a Raspberry pi.

These components supported are some of the most widely used by maker community.
There are three categories in library. Stepper motors, DC Motors and Servos.
The end user can import this library into their projects 
and then control the components with short snippets of code.
The library is modular so user can just import/use the section they need.

* Project URL: [URL LINK](https://github.com/gavinlyonsrepo/RpiMotorLib)

Installation
-----------------------------------------------

The library was tested and built on a raspberry pi 3 model b,
running Python (3.5.3) and Raspbian stretch 9.

Rpimotorlib is in the PYPI [Link](https://pypi.org/project/rpimotorlib/)
The Python Package Index (PyPI) is a repository of software for the Python programming language.

Make sure that python3 and pip3 have been installed on your machine, then for a global install:

```sh
sudo pip3 install rpimotorlib
```

Hardware
----------------------

Supported Components: 

1. Stepper motors

| Motor tested | Motor controller| Help File URL link |
| ----- | ----- | ----- |
| Unipolar 28BYJ-48 | ULN2003 driver module | [URL](Documentation/28BYJ.md)| 
| Bipolar Nema  | TB6612FNG Dual Driver Carrier | [URL](Documentation/Nema11TB6612FNG.md) |
| Bipolar Nema  | L298N H-Bridge controller module | [URL](Documentation/Nema11L298N.md) |
| Bipolar Nema  | A4988 Stepper Driver Carrier | [URL](Documentation/Nema11A4988.md)|
| Bipolar Nema  | DRV8825 Stepper Driver Carrier | [URL](Documentation/Nema11DRV8825.md) |
| Bipolar Nema  | A3967 Stepper Driver aka "easy driver v4.4" | [URL](Documentation/Nema11A3967Easy.md)|
| Bipolar (untested on hw)| LV8729 Stepper Driver Carrier  | [URL](Documentation/Nema11LV8729.md)|
| Bipolar (untested)| DV8833 Motor controller module | TODO |
| Bipolar (untested)| L9110S Motor controller module | TODO |

2. DC motors

| Motor | Motor controller| Help File URL link |
| ----- | ----- | ----- |
| DC Brushed Motor | L298N Motor controller module. | [ URL ](Documentation/L298N_DC.md) |
| DC Brushed Motor | L9110S Motor controller module. | [ URL ](Documentation/L9110S_DC.md) |
| DC Brushed Motor | DV8833 Motor controller module. | [ URL ](Documentation/DRV8833_DC.md) |
| DC Brushed Motor | TB6612FNG Dual Motor Driver Carrier| [ URL ](Documentation/TB6612FNG_DC.md) |
| DC Brushed Motor | Transistor control | [ URL ](Documentation/Transistor_DC.md) |

3. Servos (two different options see Note 3 in notes)

| Servo | Link |
| ----- | ----- |
| Servo software timing | [  RPi.GPIO module PWM ](Documentation/Servo_RPI_GPIO.md) |
| Servo hardware timing | [  pigpio library module PWM ](Documentation/Servo_pigpio.md) |


Software
-----------------------------------

1. Separate help files are in documentation folder to learn how to use library.
    Click on the relevant URL link in tables in hardware section.
2. Test files used during development are in test folder of repository.
3. There is a "Software matrix" showing which classes are used to drive which components.
    This is in the Software_Matrix.md file in documentation folder.

**Files**

rpiMotorLib files are listed below:

| File Path | Description |
| ------ | ------ |
| RPiMotorLib/RpiMotorLib.py |  stepper motor python library file |
| RPiMotorLib/rpiservolib.py | servo python library RPi.GPIO  PWM file |
| RPiMotorLib/rpi_pservo_lib.py | servo python library pigpio PWM file |
| RPiMotorLib/rpi_dc_lib.py  |    DC python motor library  file |
| documentation/*.md | 15 markdown library documentation files |
| test/*Test.py | 14 python test files |
| /usr/share/doc/RpiMotorLib/README.md | This help file |
| RPiMotorLib/RpiMotorScriptLib.py | small script with meta data about library |

A small script is installed to display version and help information.
Run the information script by typing.
RpiMotorScriptLib.py -[options]

| Option          | Description     |
| --------------- | --------------- |
| -h  | Print help information and exit |
| -v  | Print version information and exit |


**Dependencies**


1. RPi.GPIO 0.6.3  [Rpi.GPIO pypi page](https://pypi.python.org/pypi/RPi.GPIO)

A module to control Raspberry Pi GPIO channels.
This package provides a class to control the GPIO on a Raspberry Pi.
This should already be installed on most Raspberry Pis.

2. pigpio 1.64-1 [Homepage](http://abyz.co.uk/rpi/pigpio/)

This Dependency is *Optional*, it is currently 
only used in one of the two servo control options.
pigpio is a library for the Raspberry which allows 
control of the General Purpose Input Outputs (GPIO).


Notes
------------------------

1. Running two motors simultaneously.
2. Potential Issue with GPIO.cleanup() not working.
3. Servo options.

**Note 1 Running two motors simultaneously**

See github issue #11

If you want to control two steppers simultaneously, there are two basic setup
file for using threading in test folder. 

1. For Unipolar 28BYJ-48  MultiMotorThreading_BYJ.py
2. For Bipolar DRV8825 Stepper MultiMotorThreading_DRV8825.py

**Note 2 Potential Issue with GPIO.cleanup() not working** 

See github issue #18 and #21

Some users are reporting that GPIO.cleanup() does not work.
It does not switch off or "cleanup" GPIO as it should.
This is external function from RPi.GPIO. It is mainly used in the test scripts.
It is also called by the classes in DC motor if the cleanup method is passed argument "true".
If you see this issue simply don't use GPIO.cleanup() or remove GPIO.cleanup 
and clear the GPIO you set manually or use python "del" method to destroy the relevant class object,
to free resources if you need them again.

**Note 3 Servo options**

There are two different options for controlling the servo.
When using Rpi_GPIO option you may notice twitching at certain
delays and stepsizes. This is the result of the 
implementation of the RPIO PWM software timing. If the application requires
precise control the user can pick the pigpio library
which uses hardware based timing. The disadvantage being they must install 
a dependency.
