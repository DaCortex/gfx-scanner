# -*- coding: utf-8 -*-

import sys        #basic
import os

import time       #time taking

import serial     #connection to arduino

#to send a file of gcode to the printer
from printrun.printcore import printcore
from printrun import gcoder

import threading
import serial.tools.list_ports #port identification

#----- UTILITY METHODS -----#

#prints error message and quits the program
def error(message):
    
    sys.stderr.write("error(): " + message + "\n")
    sys.exit(1)

#----- MAIN -----#

def main():
    print("maintenance.py started...")

    print("Available ports")

    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print p
        #if "Arduino" in p:
        #    print "This is an Arduino!"

    
    print("Connecting to Arduino...")

    try:
        arduino = printcore('/dev/ttyACM0', 115200)  # open serial port
        time.sleep(2.0)

        print("Communication established")
    except Exception as e:
        error(str(e))

    print("Communication now possible")

    recieve(arduino)

    #set pin P4 to low (dunno why)
    # print("M42 P4 S0")
    # arduino.write("M42 P4 S0\n")
    # time.sleep(10.0)

    # #home all axis
    print("G28")
    arduino.send("G28")
    time.sleep(10.0)

    # #resetting all axis to zero          
    print("G92")
    arduino.send("G92")
    time.sleep(10.0)

    # #Linear Mode and applying values to XYZ axis | F - feedrate | S checks for endstop
    print("G1 X65 Y28 Z501 F3000 S1")
    arduino.send("G1 X65 Y28 Z501 F3000 S1")
    time.sleep(10.0)

    # #wait for current moves to finish
    print("M400")
    arduino.send("M400")
    time.sleep(10.0)

    time.sleep(5.0)

    arduino.runSmallScript("gcodescripts/18_degrees_scan.gcode")

    try:
        arduino.disconnect() # close port
        time.sleep(1.0)
        
        print("Communication terminated")
    except Exception as e:
        error(str(e))


if __name__ == '__main__':
    main()