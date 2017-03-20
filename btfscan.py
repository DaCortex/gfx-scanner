# -*- coding: utf-8 -*-

import sys        #basic
import os

import argparse   #parsing arguments
import datetime   #identification of files
import time       #time taking

#to send a file of gcode to the printer
#from printrun.printcore import printcore
#from printrun import gcoder

#import serial     #connection to arduino
#import serial.tools.list_ports #port identification

#import gphoto2 as gp #camera
import subprocess #cp in capture_image()

btfscan = sys.modules[__name__]

# GLOBALS
btfscan.INFO = False
btfscan.DEBUG = False

# CurrentWorkingDirectory
btfscan.CWD = None

# CurrentIdentification
btfscan.CID = None # 

# LOGGING [filepath: CWD/logging]
LOGGING = True
btfscan.LOGFILE = None

# CAPTURING [filepath: CWD/capturings/ID]
btfscan.CAMERA = True
btfscan.ARDUINO = True

btfscan.btfscan.GCODEFILE = []

def id():
    if btfscan.DEBUG: print("id()")

    return str(time.asctime(time.localtime(time.time())))

def setup():
    if btfscan.DEBUG: print("setup()")

    try:
        btfscan.CWD = os.getcwd()
        CID = id()

        #capturing 
        if not os.path.exists(btfscan.CWD + "/capturings"): #main folder
            os.makedirs(btfscan.CWD + "/capturings")

        capturing_path = btfscan.CWD + "/capturings/" + CID
        os.makedirs(capturing_path)


        #logging
        logging_path = capturing_path + "/logging"
        if not os.path.exists(logging_path):
            os.makedirs(logging_path)

        btfscan.LOGFILE = open(logging_path + "/" + "log" + ".txt", 'w+')
        btfscan.LOGFILE.write("Logging started at " + CID)

        return True
    except Exception as e:
        print("An error occurred:")
        print(e.what())
        return False

def open_file(FILEPATH = None):
    if btfscan.DEBUG:
        print("open_file()")
    
    try:
        btfscan.GCODEFILE = open(FILEPATH, 'r')
        return True
    except Exception as e:
        raise e

    return False

def validate_file():
    if btfscan.DEBUG: print("validate_file()")
    
    #general
    gcode_commands = 0
    camera_commands = 0
    lines = 1

    #line checking
    for line in btfscan.GCODEFILE:
        command = line.split(' ', 1)[0]
        command = command.replace(" ", "")

        #cropping command to recieve value
        value = line.replace(command + " ", "")

        if command == "Gcode":
            gcode_commands += 1

        elif command == "Picture":
            camera_commands += 1
        else:
            print("Error in line: " + str(lines))
            print("   Given line: "  + line)
            sys.exit(1)

        lines += 1

    #info pring
    if btfscan.INFO:
        print("File info:")

    return True

def main():
    #if btfscan.DEBUG: print("main()")

    filepath = None
    # argument parsing
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
    elif len(sys.argv) == 3:
        filepath = sys.argv[1]
        info = sys.argv[2]

        if "info" in info:
            btfscan.INFO = True
            print("Console output is now set to INFO.")

        if "testing" in info: #no camera & arduino attached
            btfscan.INFO = True
            btfscan.DEBUG = True
            CAMERA = False
            ARDUINO = False
            print("No arduino & camera connection will be established.")

        if "debug" in info:
            btfscan.INFO = True
            btfscan.DEBUG = True
            print("Console output is now set to DEBUG.")


    else:
        print("Invalid amount of arguments")

    # setup
    if btfscan.INFO:
        print("Arguments were parsed.")
        print("Setting everything up.")

    if not setup():
        print("Incomplete setup.")
        sys.exit(1)

    # file opening and validation
    if not open_file(filepath):
        print("Unable to open file.")
        sys.exit(1)

    if not validate_file():
        print("Invalid file.")
        sys.exit(1)

    if btfscan.INFO:
        print("File is parsed and loaded.")
        print("Starting btf loop.")
    
    # loop

    #run_script()



if __name__ == '__main__':
    main()