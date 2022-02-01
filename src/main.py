'''!
@file       main.py
@brief      
@details    
@author     Jakob Frabosilio
@date       01/11/2022
'''
from pyb import USB_VCP
import pyb
from Lab1EncoderClass import EncoderClass
from Lab1MotorDriver import MotorDriver
from Lab2ClosedLoop import ClosedLoop
import utime

## Serial bus used to communicate with PC
myUSB = USB_VCP()

## Encoder object (Channel A pin, Channel B pin, Timer)
testEncoder = EncoderClass(pyb.Pin.board.PB6, pyb.Pin.board.PB7, 4)

## Motor object (INT pin, Motor+ pin, Motor- pin, Timer)
testMotor = MotorDriver(pyb.Pin.board.PA10, pyb.Pin.board.PB4, pyb.Pin.board.PB5, 3)

## Closed loop controller object (Kp value)
testLoop = ClosedLoop(0.92)

## Beginning time for each step response loop
stepTime = 0

## Beginning time for each encoder read loop
encTime = 0

## Number of times step response has been called (dictates set position)
loopCount = 1

## Reference position that motor should set to
refPos = 0

## Actual motor position as interpreted by encoder
actPos = 0

## Current time since program initialization (used for plotting)
plotTime = 0

## State tracking variable
state = 0

## Duty cycle variable
setDuty = 0


if __name__ == "__main__":
    while True:
        try:

# ----- WAITING STATE -----
            if state == 0:
                if myUSB.any():                                # Checks if any chars have been sent over USB
                    userInput = myUSB.read(1).decode()         # If so, reads char and assigns it to variable
                    
                    # Input G or g to start data collection
                    if userInput == 'g' or userInput == 'G':
                        stepTime = utime.ticks_ms()            # Starts step response loop and encoder loop 'timers'
                        encTime = utime.ticks_ms()
                        state = 1
                        refPos = 360*loopCount                 # Sets position to increments of 360 degrees (1 rev) for each step response
                                                               # (currently stays at 360, doesn't increment)
                        testEncoder.zero()
                        
                    # Input X or x to enter Kp input state
                    elif userInput == 'x' or userInput == 'X':
                        state = 3
                        myUSB.write('Input Kp value below. Must not exceed four characters.'.encode())
                        
                        
# ----- STEP RESPONSE STATE -----

            elif state == 1:
                if utime.ticks_diff(utime.ticks_ms(), stepTime) < 750:                      # 
                    if utime.ticks_diff(utime.ticks_ms(), encTime) >= 10:
                        actPos = testEncoder.update()                                       # Queries actual position by updating encoder
                        plotTime = utime.ticks_diff(utime.ticks_ms(), stepTime)             # Calculates time since intitialization for plotting
                        setDuty = testLoop.update(refPos, actPos, plotTime, saveData=True)  # Uses closed-loop controller to set duty cycle
                        testMotor.set_duty_cycle(setDuty)                                   # Sets motor duty to closed-loop controller set
                        encTime = utime.ticks_ms()                                          # Resets encoder loop time
                else:
                    # loopCount += 1
                    testMotor.set_duty_cycle(0)
                    endTime = utime.ticks_ms()
                    state = 2
                        
            elif state == 2: # data send state
                for times in testLoop.timeVals:
                    myUSB.write(str(times).encode())
                    myUSB.write(','.encode())
                myUSB.write('|'.encode())
                for refs in testLoop.refVals:
                    myUSB.write(str(refs).encode())
                    myUSB.write(','.encode())
                myUSB.write('|'.encode())
                for meas in testLoop.measVals:
                    myUSB.write(str(meas).encode())
                    myUSB.write(','.encode())
                myUSB.write('|'.encode())
                myUSB.write(str(testLoop.Kp).encode())
                myUSB.write('\n'.encode())
                testLoop.clearResults()
                state = 0
                
            elif state == 3: # KP set state
                
                # Waits for an additional input to set Kp
                if myUSB.any():                               # Checks if any chars have been sent over USB
                    try:
                        userInput = myUSB.read(4).decode()
                        testLoop.setKp(float(userInput))
                        myUSB.write('Kp set to: '.encode())
                        myUSB.write(str(float(userInput)).encode())
                        
                        state = 0
                    except:
                        break
        except:
            break