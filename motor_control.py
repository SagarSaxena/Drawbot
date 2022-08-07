#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import math

# stepper params
DEGREES_PER_STEP = 1.8
DELAY_BETWEEN_STEPS = 0.002

# pin nummbers
enableA_pin = 4
coil_A_1_pin = 22
coil_A_2_pin = 27
coil_B_1_pin = 24
coil_B_2_pin = 23
enableB_pin = 25

# use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# turn off warnings
GPIO.setwarnings(False)

# setup IO ports as outputs
GPIO.setup(enableA_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT) #red wire
GPIO.setup(coil_A_2_pin, GPIO.OUT) #blue wire
GPIO.setup(coil_B_1_pin, GPIO.OUT) #yellow wire
GPIO.setup(coil_B_2_pin, GPIO.OUT) #white wire
GPIO.setup(enableB_pin, GPIO.OUT)

# set ports
GPIO.output(enableA_pin, GPIO.HIGH)
GPIO.output(enableB_pin, GPIO.HIGH)

# https://secure.sayal.com/STORE2/View_SHOP.php?SKU=162138
# Excitation sequence:
# Step             1 2 3 4
# Red/A_1_pin      + + - -
# Yellow/B_1_pin   - + + -
# Blue/A_2_pin     - - + +
# White/B_2_pin    + - - +
STEP_SEQUENCE = [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]

currentStepIndex = 0

def rotateByAngle(angleInRadians, delay):
    global currentStepIndex
    steps = calculateNumOfSteps(angleInRadians)
    direction = int (angleInRadians / abs(angleInRadians))
    i = 0
    while i in range(0, steps):
        nextStep(STEP_SEQUENCE[currentStepIndex])
        time.sleep(delay)
        currentStepIndex = (currentStepIndex + direction) % 4
        i += 1

def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin, w1)
    GPIO.output(coil_B_1_pin, w2)
    GPIO.output(coil_A_2_pin, w3)
    GPIO.output(coil_B_2_pin, w4)

def calculateNumOfSteps(angleInRadians):
    numSteps = int(abs(angleInRadians)*180/math.pi/DEGREES_PER_STEP)
    return numSteps 

def nextStep(stepTable):
    GPIO.output(coil_A_1_pin, stepTable[0])
    GPIO.output(coil_B_1_pin, stepTable[1])
    GPIO.output(coil_A_2_pin, stepTable[2])
    GPIO.output(coil_B_2_pin, stepTable[3])

while True:
    user_angle = input("Move by how many radians? ")
    rotateByAngle(float(user_angle), DELAY_BETWEEN_STEPS)

# clean up used ports
GPIO.cleanup()










#def moveCW(delay, steps):
#    i = 0
#    while i in range(0, steps):
#        setStep(1, 0, 0, 1)
#        time.sleep(delay)
#        setStep(1, 1, 0, 0)
#        time.sleep(delay)
#        setStep(0, 1, 1, 0)
#        time.sleep(delay)
#        setStep(0, 0, 1, 1)
#        time.sleep(delay)
#        i += 1

#def moveCCW(delay, steps):
#    i = 0
#    while i in range(0, steps):
#        setStep(0, 0, 1, 1)
#        time.sleep(delay)
#        setStep(0, 1, 1, 0)
#        time.sleep(delay)
#        setStep(1, 1, 0, 0)
#        time.sleep(delay)
#        setStep(1, 0, 0, 1)
#        time.sleep(delay)
#        i += 1



