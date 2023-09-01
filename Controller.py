import pygame
import threading
import concurrent.futures
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import cv2

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)

pygame.init()
js = pygame.joystick.Joystick(0)
js.init()
clock = pygame.time.Clock()

direction = [22, 17]
step = [23, 18]
en = [24, 27]
msx = [(26, 21, 20), (16, 19, 13)]

motors = [RpiMotorLib.A4988Nema(direction[i], step[i], msx[i], "DRV8825") for i in range(2)]

GPIO.setup(en[0],GPIO.OUT)
GPIO.setup(en[1],GPIO.OUT)
GPIO.output(en[0],GPIO.LOW)
GPIO.output(en[1],GPIO.LOW)

LEFT, RIGHT, UP, DOWN = False, False, False, False
SPEED = 4
SPEEDS = ["Full", "Half", "1/4", "1/8", "1/16", "1/32"]

def increase_speed():
    global SPEED
    SPEED = (SPEED + 1) % len(SPEEDS)
    print(f"Speed is now {SPEEDS[SPEED]}")

def decrease_speed():
    global SPEED
    SPEED = (SPEED - 1) % len(SPEEDS)
    print(f"Speed is now {SPEEDS[SPEED]}")

def rotate():# True=Clockwise, False=Counter-Clockwise, axis=0 for y, 1 for x
    with concurrent.futures.ThreadPoolExecutor() as executor:
        if LEFT:
            executor.submit(motors[1].motor_go, False, SPEEDS[SPEED] , 2, .0005, False)
        elif RIGHT:
            executor.submit(motors[1].motor_go, True, SPEEDS[SPEED] , 2, .0005, False)
        if UP:
            executor.submit(motors[0].motor_go, False, SPEEDS[SPEED] , 2, .0005, False)
        elif DOWN:
            executor.submit(motors[0].motor_go, True, SPEEDS[SPEED] , 2, .0005, False)

while True:
    clock.tick(120)

    res, image = cam.read()
    image = cv2.rotate(image, cv2.ROTATE_180)
    cv2.imshow("image", image)
    cv2.waitKey(1)

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

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 7 or event.button == 6:
                pygame.quit()
                GPIO.cleanup()
                exit()
                
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                increase_speed()
                increase_speed()
            elif event.button == 3:
                decrease_speed()
                decrease_speed()
            elif event.button == 1:
                decrease_speed()
            elif event.button == 2:
                increase_speed()
                
        elif event.type == pygame.QUIT:
            pygame.quit()
            GPIO.cleanup()
            exit()
            
    rotate()