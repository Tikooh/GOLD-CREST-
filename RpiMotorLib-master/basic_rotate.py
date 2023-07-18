import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib


'''
Change the below to match the actual pins used for the motors.

May have to attach this part to the main processing python script and then hand these in as parameters.
'''
GPIOx_pins = (14, 15, 18)
directionx = 20
stepx = 21

GPIOy_pins = (13, 16, 17)
directiony = 22
stepy = 23

motorx = RpiMotorLib.A4988Nema(directionx, stepx, GPIOx_pins, "DRV8825")
motory = RpiMotorLib.A4988Nema(directiony, stepy, GPIOy_pins, "DRV8825")

def rotate(bbox_x: float, bbox_y: float, view_width: int, view_height: int, motorx , motory):
    '''
    Bbox co-ordinates are the midpoints of the co-ordinates. 

    CHANGE THE CLOCKWISE TRUE/FALSE AS NEEDED TO OUR MODEL
    '''
    if bbox_x < (view_width/2):
        x_clockwise = False
    else:
        x_clockwise = True

    if bbox_y < (view_height/2):
        y_clockwise = False
    else:
        y_clockwise = True

    motorx.motor_go(x_clockwise, "1/32", 100)
    motory.motor_go(y_clockwise, "1/32", 100)