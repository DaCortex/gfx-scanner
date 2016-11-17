# -*- coding: utf-8 -*-

import sys        #basic
import os

import time       #time taking

import serial     #connection to arduino
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
        serial_connection = serial.Serial('/dev/ttyACM0' , 115200)  # open serial port
        time.sleep(1.0)

        print("Communication established")
    except Exception as e:
        error(str(e))




    #set pin P4 to low (dunno why)
    serial_connection.write("M42 P4 S0\n")
    time.sleep(1.0)

    #home all axis
    serial_connection.write("G28\n")
    time.sleep(1.0)

    #resetting all axis to zero          
    serial_connection.write("G92\n")
    time.sleep(1.0)

    #Linear Mode and applying values to XYZ axis | F - feedrate | S checks for endstop
    serial_connection.write("G1 X65 Y28 Z501 F3000 S1\n")
    time.sleep(1.0)

    #wait for current moves to finish
    serial_connection.write("M400\n")
    time.sleep(1.0)

    waiting = 10.0

    time_1 = float(round(time.time()))

    run = True
    while(run):
        data = serial_connection.readline()

        if data:
            print(str(data))
        
        time_2 = float(round(time.time()))

        time_left = time_2 - time_1

        user_input = ""
        if time_left > waiting:
            user_input = raw_input("Some input please: ")

            # Now do something with the above
            serial_connection.write(str(user_input))

        #input validation
        if user_input == "quit":
            run = False
            print("Quitting main loop...")

        time.sleep(0.1)


    f = open("gcodescripts/9degree.gcode")
    for line in f:
        print(line)
        serial_connection.write(str(line))

        data = serial_connection.readline()

        if data:
            print(str(data))
    f.close()

    time.sleep(5.0)

    try:
        serial_connection.close() # close port
        time.sleep(1.0)
        
        print("Communication terminated")
    except Exception as e:
        error(str(e))


if __name__ == '__main__':
    main()