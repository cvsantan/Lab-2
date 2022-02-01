'''!
@file       Lab2FrontEnd.py
@brief      
@details    
@author     Jakob Frabosilio
@date       01/11/2022
'''

import time
import serial
import matplotlib.pyplot as myPlot
import matplotlib.ticker as ticker

def sendChar():
    ''' Triggers an input command that sends an ASCII character through the serial bus
    @return     Returns the uppercase variant of the inputted character.
    '''
    inv = input('Input: ')
    if inv.upper() != 'H':
        ser.write(str(inv).encode('ascii'))
    return inv.upper()

def cmdsMsg():
    ''' Prints the list of possible inputs
    '''
    print('\nCHARACTER | ACTION')
    print('  G / g   | Step response activate.')
    print('  S / s   | Send data to serial and reset.')
    print('  X / X   | Set value of Kp')

ser = serial.Serial(port='COM8',baudrate=115273,timeout=1)

startTime = time.time()
state = 0

## String that holds raw string data sent from Nucleo, from data collection state
csvList = ''

## String containing stripped csvList string data
strippedString = ''

## String containing split and cleaned strippedString data
splitStrings = ''

## Length of each data array (time, position, etc.)
arrLen = 0

cmdsMsg()

while True:
    if state == 0: # input state
        # If one second has not elapsed since last input, wait until it has.
        # This allows time for the Nucleo to send serial data over the
        # serial bus and is a UX decision for the user.
        if time.time() - startTime > 1 and ser.in_waiting == 0:
            myChar = sendChar()
            if myChar == 'S':
                startTime = time.time()
                state = 1
                print('please')
            else:
                cmdsMsg()
            startTime = time.time()
        elif ser.in_waiting != 0:
            print(ser.readline().decode('ascii'))

    elif state == 1: # data collection
        if time.time() - startTime > 1.5:
            while ser.in_waiting != 0:
                csvList += ser.read().decode()
            if ser.in_waiting == 0:
                state = 2
                print('work')
            startTime = time.time()
            
    elif state == 2:
        splitCSV = csvList.split('|')
        timeVals = splitCSV[0].split(',')
        refVals = splitCSV[1].split(',')
        measVals = splitCSV[2].split(',')
        timeVals.pop()
        refVals.pop()
        measVals.pop()
        print(len(timeVals))
        print(timeVals)
        print(refVals)              
        print(measVals)
        if timeVals != ['']:
            fig, ax = myPlot.subplots(1, 1)
            x_tick_spacing = 20
            #y_tick_spacing = 
            #myPlot.xticks(np.arange(int(timeVals[0]), int(timeVals[len(timeVals)-1]), len(timeVals)/100))
            #myPlot.yticks(np.arange(0, max(y), 2))
            #myPlot.xticks(range(int(timeVals[0]),int(timeVals[len(timeVals)-1]),200))
            ax.plot(timeVals, measVals, color = 'k', ls = '-', label = 'Measured Values')
            ax.plot(timeVals, refVals, color = 'k', ls = ':', label = 'Reference Values')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_spacing))
            #ax.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_spacing))
            myPlot.xlabel('Time (ms)')                     # sets axes labels
            myPlot.ylabel('Position (degrees)')
            myPlot.legend()                                     # turns on legend
            myPlot.show()
        state = 0
  
