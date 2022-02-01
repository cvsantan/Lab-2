'''!
@file       Lab1MotorDriver.py
@brief      Class for motor driver from Lab #1: Gray Area instructions
@details    Calling this class creates a motor driver object that can
            be used to control a motor using an H-bridge
@author     Jakob Frabosilio
@date       01/11/2022
'''

import pyb

class MotorDriver:
    '''!
    This class implements a motor driver for an ME405 project.
    '''
    
    def __init__(self, en_pin, in1pin, in2pin, timer):
        '''!
        Creates a motor driver by initializing GPIO pins and turning the motor off
        for safety.
        @param en_pin     A pyb.Pin object for the EN/OCD "toggle" pin
        @param in1pin     A pyb.Pin object for the 
        @param in2pin     
        @param timer      
        '''
        
        self.en_pin = pyb.Pin(en_pin, pyb.Pin.PULL_UP)
        self.in1pin = pyb.Pin(in1pin, pyb.Pin.OUT_PP)
        self.in2pin = pyb.Pin(in2pin, pyb.Pin.OUT_PP)
        self.tim = pyb.Timer(timer,freq = 20000)
        self.mPos = self.tim.channel(1, pyb.Timer.PWM, pin=self.in1pin)
        self.mNeg = self.tim.channel(2, pyb.Timer.PWM, pin=self.in2pin)
        self.en_pin.high()
        self.mPos.pulse_width_percent(0)
        self.mNeg.pulse_width_percent(0)
        
        
    def set_duty_cycle(self, level):
        '''!
        Sets the duty cycle of the motor to the given level. Positive values cause
        torque in one direction, negative values cause torque in opposite direction.
        @param level
        '''
        
        if level < 0 and level >= -100:
            self.mPos.pulse_width_percent(0)
            self.mNeg.pulse_width_percent(-level)
        elif level >= 0 and level <= 100:
            self.mPos.pulse_width_percent(level)
            self.mNeg.pulse_width_percent(0)