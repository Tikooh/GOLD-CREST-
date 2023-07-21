import pygame
import threading
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
pygame.init()
direction = [22, 17]
step = [23, 18]
en = [24, 27]
motors = [RpiMotorLib.A4988Nema(direction[i], step[i], (21,21,21), "DRV8825") for i in range(2)]
GPIO.setup(en[0],GPIO.OUT)
GPIO.setup(en[1],GPIO.OUT)
GPIO.output(en[0],GPIO.LOW)
GPIO.output(en[1],GPIO.LOW)
js = pygame.joystick.Joystick(0)
js.init()
clock = pygame.time.Clock()
LEFT, RIGHT, UP, DOWN = False, False, False, False
def rotate(direction, axis):# True=Clockwise, False=Counter-Clockwise, axis=0 for y, 1 for x
    threading.Thread(target=motors[axis].motor_go, args=(direction, "Full" , 1, .0005, False, 0.05), daemon=True).start()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value > 0.5:
                    LEFT, RIGHT = False, True
                elif event.value < -0.5:
                    LEFT, RIGHT = True, False
                else:
                    LEFT, RIGHT = False, False
            elif event.axis == 1:
                if event.value > 0.5:
                    UP, DOWN = False, True
                elif event.value < -0.5:
                    UP, DOWN = True, False
                else:
                    UP, DOWN = False, False
        elif event.type == pygame.QUIT or event.type == pygame.JOYBUTTONDOWN:
            pygame.quit()
            GPIO.cleanup()
            exit()
    if UP:
        rotate(False, 0)
    elif DOWN:
        rotate(True, 0)
    if LEFT:
        rotate(False, 1)
    elif RIGHT:
        rotate(True, 1)

