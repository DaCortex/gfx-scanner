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

#----- SERIAL METHODS -----#

def recieve(message, serial):
    data = serial.readline()

    if data:
        message = data
    else:
        message = ""

def send(command, serial, callback = "None", PrintCallback = False):
    #check for endline \n

    if "\n" not in command:
        command += "\n"

    serial.write(command)

    time.sleep(0.1)

    if callback is not "None": 
        
        recieve(callback, serial)

    if PrintCallback is not False:
        callback = callback.replace('\n','')
        print("Command: " + command + " Callback: " + callback)

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
        arduino = serial.Serial('/dev/ttyACM0' , 115200)  # open serial port
        time.sleep(1.0)

        print("Communication established")
    except Exception as e:
        error(str(e))



    str_callback = ""

    #set pin P4 to low (dunno why)
    send("M42 P4 S0", arduino, str_callback, PrintCallback = False)

    #home all axis
    send("G28", arduino, str_callback, PrintCallback = False)

    #resetting all axis to zero          
    send("G92", arduino, str_callback, PrintCallback = False)

    #Linear Mode and applying values to XYZ axis | F - feedrate | S checks for endstop
    send("G1 X65 Y28 Z501 F3000 S1", arduino, str_callback, PrintCallback = False)

    #wait for current moves to finish
    send("M400", arduino, str_callback, PrintCallback = False)

    waiting = 10.0

    time_1 = float(round(time.time()))

    run = True
    while(run):
        data = arduino.readline()

        if data:
            print(str(data))
        
        time_2 = float(round(time.time()))

        time_left = time_2 - time_1

        user_input = ""
        if time_left > waiting:
            user_input = raw_input("Some input please: ")

            # Now do something with the above
            arduino.write(str(user_input))

        #input validation
        if user_input == "quit":
            run = False
            print("Quitting main loop...")

        time.sleep(0.1)


    f = open("gcodescripts/9degree.gcode")
    for line in f:
        send(line, arduino, str_callback, PrintCallback = True)

    f.close()

    time.sleep(5.0)

    try:
        arduino.close() # close port
        time.sleep(1.0)
        
        print("Communication terminated")
    except Exception as e:
        error(str(e))


if __name__ == '__main__':
    main()