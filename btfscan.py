# -*- coding: utf-8 -*-

import sys        #basic
import os
import inspect 

import argparse   #parsing arguments
import datetime   #identification of files
import time       #time taking

import serial     #connection to arduino
import serial.tools.list_ports #port identification

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
btfscan.PRINTCORE = None

btfscan.GCODEFILE = []

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
            if INFO: print("Creating main folder: " + btfscan.CWD + "/capturings")

        capturing_path = btfscan.CWD + "/capturings/" + CID
        os.makedirs(capturing_path)
        if INFO: print("Creating current folder: " + capturing_path)


        #logging
        logging_path = capturing_path + "/logging"
        if not os.path.exists(logging_path):
            os.makedirs(logging_path)
            if INFO: print("Creating logging folder: " + logging_path)

        btfscan.LOGFILE = open(logging_path + "/" + "log" + ".txt", 'w+')
        btfscan.LOGFILE.write("Logging started at " + CID)
        if INFO: print("Creating logfile: " + logging_path + "/" + "log" + ".txt")


        #listing ports
        print("Available ports")
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print(p)
            if "Arduino" in p:
                print("Found Arduino at: " + str(p))

        print("Connecting to printer")
        #printer
        #printcore
        btfscan.PRINTCORE = printcore('/dev/ttyACM0', 115200)

        return True
    except Exception as e:
        print("An error occurred:")
        print(e)
        return False

def open_file(FILEPATH = None):
    if btfscan.DEBUG: print("open_file(" + FILEPATH + ")")
    
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

#recieves a method and calls it in a safe code section

def validity_callback(METHOD):
    if btfscan.DEBUG: print("validity_callback()")
    try:
        METHOD()
        return True
    except Exception as e:
        print("An error occurred:")
        raise e

def run_loop():

    run = True
    while run:
        #btfscan.PRINTCORE.
        pass

    return True

def run_init(FILENAME):
    if btfscan.DEBUG: print("run_init(" + FILENAME + ")")

    gcode = [i.strip()for i in open(FILENAME)]

    print("Given initial gcode script:")
    print(gcode)

    gcode = gcoder.LightGCode(gcode)

    btfscan.PRINTCORE.startprint(gcode)

# modes = {"testing" : set_testing}

# def set_mode(MODE = ""):

#     if MODE in modes:
#         print("Found mode")
#         modes[MODE]()

def main():

    filepath = None

    # argument parsing
    if len(sys.argv) == 2:
        filepath = sys.argv[1]
        btfscan.INFO = True
        print("Console output is set to INFO.")

    elif len(sys.argv) == 3:
        filepath = sys.argv[1]
        extra = sys.argv[2]

        if "testing" in extra: #no camera & arduino attached
            btfscan.INFO = True
            btfscan.DEBUG = True
            btfscan.CAMERA = False
            btfscan.ARDUINO = False
            print("No arduino & camera connection will be established.")

        elif "debug" in extra:
            btfscan.INFO = True
            btfscan.DEBUG = True
            print("Console output is set to DEBUG.")

        else:
            print("Importing printcore..")
            #to send a file of gcode to the printer
            from printrun.printcore import printcore
            from printrun import gcoder


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
    
    run_init("init.gcode")

    # loop
    #run_loop()

if __name__ == '__main__':
    main()