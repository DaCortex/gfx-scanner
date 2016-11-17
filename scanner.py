# -*- coding: utf-8 -*-

import sys        #basic
import os

import argparse   #parsing arguments
import datetime   #identification of files
import time       #time taking
import serial     #connection to arduino
import serial.tools.list_ports #port identification

import gphoto2 as gp #camera
import subprocess #cp in capture_image()


#----- GLOBALS & FLAGS -----#
#for basic testing when there is no real system attatched
CAMERA = False
ARDUINO = False
SCANNING = True
VALIDATION = True

#print info after x pictures
INFO_INTERVAL = 0.2 #percent

DATATYPE = ".gcode"


#----- UTILITY METHODS -----#

#prints error message and quits the program
def error(message):
    
    sys.stderr.write(message + "\n")
    sys.exit(1)

#returns current time for identification
def id():
    return str(time.asctime(time.localtime(time.time())))

def user_validation(message, yes, no):
    if(VALIDATION):
        print("\n" + message + "\n")
        check = None
        while(not (check == yes)):
            check = raw_input()
            #print("Your input: " + str(check))
            if(check == no):
                error("Exiting program...\n")
            elif(check != yes):
                print("Wrong input: " + check)

#----- CAMERA METHODS -----#

def capture_image( context, camera, filepath):
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE, context))

    target = os.path.join('/tmp', file_path.name)
    
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, context))
    
    gp.check_result(gp.gp_file_save(camera_file, target))

    subprocess.call(['cp', target,filepath])


#----- ARDUINO METHODS -----#

#def send():

#def recieve():


#----- COMPUTATIONAL METHODS -----#

#returns the amount of shots that need to be taken
def compute_shots(degree):
    
    #positions per variable
    light       = 180 / degree
    first_axis  = 360 / degree
    second_axis = 360 / degree

    #compute all  possible positions
    shots = light * first_axis * second_axis

    return shots

#returns the position of all motors given by the
def compute_position( current_shot, overall_shots, degree):

    return 5




#----- MAIN -----#

def main():


#-----[0] basic setup-----#

    #serial connection to arduino
    serial_connection = None 

    #argument parser
    parser = argparse.ArgumentParser()

    #directory organization
    current_directory = os.getcwd()

    if not os.path.exists(current_directory + "/capturings"):
        print("Creating output folder...")
        os.makedirs(current_directory + "/capturings/")

    current_folder = current_directory + "/capturings/capturing: " + id() + "/"

    if not os.path.exists(current_folder):
        os.makedirs(current_folder)

#-----[1] basic input validation-----#

    parser.add_argument("filename", help="scan is executed with given file", type=str)

    args = parser.parse_args()

    #datatype validation
    filename = args.filename
    file = None
    if not(filename[len(filename)-len(DATATYPE) :] == DATATYPE):
        error_str = "[Error] Wrong datatype\n"
        error(error_str + usage_str)

    #filename validation
    if not(len(filename) > len(DATATYPE)):
        error_str = "[Error] No filename given\n"
        error(error_str + usage_str)

    #check whether the file exists
    try:
        f = open(filename, 'r')

        #reading file
        file = f.readlines()
        f.close()
    except FileNotFoundError:
        error_str =  "[Error] " + filename + " no such file or directory\n"
        error_str += "         Execute filegenerator.py\n"
        error(error_str + usage_str)     

    #check whether the file is empty
    if(file == ""):
        error_str = "[Error] The given file is empty\n"
        error(error_str + usage_str)


#-----[2] analyzing and validating input file-----#
    print("Analyzing input file...\n")

    command_a = 0   #arduino
    command_c = 0   #camera
    command_u = 0   #unknown

    for line in file:
        command = line.split(' ', 1)[0]
        command = command.replace(" ", "")

        #cropping command to recieve value
        value = line.replace(command + " ", "")

        if command == "Gcode":
            command_a += 1

        elif command == "Picture":
            command_c += 1
        else:
            command_u += 1
            print("Unknown command: " + command + " value: " + value)

    lines = len(file)
    interval = int(command_c * INFO_INTERVAL)

    print("   Overall lines: " +  str(lines))
    print("   Info interval: " +  str(interval))
    print("")
    print("Overall Pictures: " +  str(command_c))
    print("Arduino commands: " +  str(command_a))
    print("Unknown commands: " +  str(command_u))
    print("")



#-----[3] connecting & testing arduino & apparatus-----#
    if(ARDUINO):

        print("Connecting to Arduino...\n")

        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            print p
            if "Arduino" in p:
                print "This is an Arduino!"

        try:
            serial_connection = serial.Serial('/dev/ttyACM0')  # open serial port
        except Exception as e:
            error(str(e))
        
        #recieving MarlinRC output
        print("Waiting for MarlinRC output...\n")
        waiting = 15.0

        time_1 = float(round(time.time()))

        run = True
        while(run):
            data = serial_connection.readline()

            if data:
                print(str(data))
            
            time_2 = float(round(time.time()))

            time_left = time_2 - time_1

            if time_left > waiting:
                message =   "Please check for MarlinRC warnings etc.\n" + \
                            "Type 'ok' to proceed if everything is fine.\n" + \
                            "Type 'end' to end program. For further investigations, check: maintenance.py\n"

                user_validation(message, "ok", "end")

            time.sleep(0.1)

        #moving the apparatus
        print("Initiating Apparatus...\n")
        try:
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

        except Exception as e:
                exit(str(e))
   
    else:
        print("WARNING: ARDUINO-Flag is set to False")

#-----[4] connecting & testing camera-----#

    if(CAMERA):

        print("Connecting to Camera...\n")
        try:
            gp_context =   gp.gp_context_new()
            gp_camera  =   gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(gp_camera, gp_context))

            print(str(gp_camera.get_summary(gp_context)))

        except Exception as e:
            exit(str(e))
        
        print("Testing Camera...\n")
        try:
            #some test photos
            for x in range( 0, 5):
                filepath = current_folder + "/test_" + str(x) + ".jpg"
                #filepath = current_folder + "/test_" + str(x) + ".raw"

                capture_image(gp_context, gp_camera, filepath)

        except Exception as e:
                exit(str(e))

    else:
        print("WARNING: CAMERA-Flag is set to False")


    #waiting for user input, that everything worked the right way
    message =   "Type 'ok' to validate that Camera & Apparatus are working correctly.\n" + \
                "Type 'end' to end program. For further investigations, check: maintenance.py\n"

    #some input here
    user_validation(message, "ok", "end")


#-----[5] scanning material-----#
    # f = open("gcodescripts/9degree.gcode")
    # for line in f:
    #     print(line)
    #     serial_connection.write(str(line))

    #     data = serial_connection.readline()

    #     if data:
    #         print(str(data))
    # f.close()

    if not SCANNING: error("Warning: SCANNING-Flag is set to False")
    if not ARDUINO:  print("WARNING: ARDUINO-Flag is set to False")
    if not CAMERA:   print("WARNING: CAMERA-Flag is set to False")

    print("Pre-Capturing info:")
    print("Overall  Pictures: " +  str(command_c))
    print("Info output after: " +  str(interval))

    message = "Do you want to scan? Type: yes or no\n"

    user_validation(message, "yes", "no")

    time.sleep(5.0)
    print("Capturing...\n")
    time.sleep(5.0)
    print("Started: " + time.asctime(time.localtime(time.time())))

    #pre-computations and definitions
    #overall_shots = compute_shots(degree) #counting Picture in files
    time_average  = 0.0 # Seconds
    time_started  = float(time.time()) # Seconds
    time_last = time_started

    i = 0

    for line in file:
        print(str(i))
        i = i +1
        command = line.split(' ', 1)[0]
        command = command.replace(" ", "")
        print("Command: " + command)
        #cropping command to recieve value
        value = line.replace(command + " ", "")
        print("Value: " + value)

        #setting current motor positions
        if command == "Gcode":
            if(ARDUINO):
                if "\n" not in command:
                    command += "\n"
                serial_connection.write(command)
            else:
                time.sleep(0.1) # just simulating

        #taking and saving picture
        elif command == "Picture":
            #capturing
            if(CAMERA):
                current_filepath = current_folder + value + ".raw"

                capture_image(gp_context, gp_camera, current_filepath)

                #validating, that picture is saved
                if not os.path.exists(current_filepath):
                    error("File not saved.")

            #explanation:
            # a photo has been taken, now a new task starts:
            # sending commands to arduino, taking picture etc.
            # but before: computing the taken time

            #time taking
            time_now = float(round(time.time()))

            if(time_average == 0.0):  #first time taking
                time_average = time_now - time_last
            else:                   #every other case of time taking
                tmp_time_average = time_now - time_last
                time_average = (time_average + tmp_time_average) / 2.0
            
            time_last = time_now #reset to new time taking

        else:
            error("Unknown command: " + command)

        #informational print
        if((i % interval) == 0): #time to print some info
            time_now = float(round(time.time()))

            passed_time = time_now - time_started

            print("Average time for a picture: " + str(round(time_average)) + " Seconds")
            print("               Passed time: " + str(round(passed_time))  + " Seconds")
            #print("     Left time (estimated): " + str(round(time_left))    + " Seconds")


    print("Finished: " + time.asctime(time.localtime(time.time())))


#-----[6] cleaning up-----#
    #arduino
    if(ARDUINO):
        serial_connection.close() # close port
    
    #camera
    if(CAMERA):
        gp.check_result(gp.gp_camera_exit(gp_camera, gp_context))


if __name__ == '__main__':
    main()