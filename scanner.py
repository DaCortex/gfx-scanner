# -*- coding: utf-8 -*-

import sys        #basic
import os

import argparse   #parsing arguments
import datetime   #identification of files
import time       #taking time for averaging a shot
import serial     #connection to arduino

import gphoto2 as gp #camera
import subprocess #cp in capture_image()

#----- UTILITY METHODS -----#

#prints error message and quits the program
def error(message):
    
    sys.stderr.write("error(): " + message + "\n")
    sys.exit(1)

#returns current time for identification
def id():
    return str(time.asctime(time.localtime(time.time())))

#----- GLOBALS & FLAGS -----#
#for basic testing when there is no real system attatched
CAMERA = False
ARDUINO = False

#print info after x pictures
INFO_INTERVAL = 10

LOG_FILENAME = 'scanner' + id() + '.log'


#----- METHODS -----#

def capture_image( context, camera, filepath):
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE, context))

    target = os.path.join('/tmp', file_path.name)
    
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, context))
    
    gp.check_result(gp.gp_file_save(camera_file, target))

    subprocess.call(['cp', target,filepath])

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

    parser.add_argument("degree", help="scan is executed with given degrees", type=int)

    args = parser.parse_args()

    #1: degree
    degree = args.degree
    if(360%degree != 0):
        error("Degree must be integer divider of 360° (Used: " + str(degree) + ")")


#-----[2] connecting & testing arduino & apparatus-----#
    if(ARDUINO):

        print("Connecting to Arduino...")
        try:
            serial_connection = serial.Serial('/dev/ttyUSB0')  # open serial port
        except Exception as e:
            error(str(e))

        #moving the apparatus
        print("Testing Apparatus...")
        try:
            #set pin P4 to low (dunno why)
            serial_connection.write("M42 P4 S0\n")

            #home all axis
            serial_connection.write("G28")

            #resetting all axis to zero          
            serial_connection.write("G92")

            #Linear Mode and applying values to XYZ axis | F - feedrate | S checks for endstop
            serial_connection.write("G1 X65 Y28 Z501 F3000 S1")

            #wait for current moves to finish
            serial_connection.write("M400")

        except Exception as e:
                exit(str(e))

    else:
        print("WARNING: ARDUINO-Flag is set to False")

#-----[3] connecting & testing camera-----#

    if(CAMERA):

        print("Connecting to Camera...")
        try:
            gp_context =   gp.gp_context_new()
            gp_camera  =   gp.check_result(gp.gp_camera_new())
            gp.check_result(gp.gp_camera_init(gp_camera, gp_context))

        except Exception as e:
            exit(str(e))
        
        print("Testing Camera...")
        try:
            #some test photos
            for x in range( 0, 5):
                filepath = current_folder + "/test_" + str(x) + ".jpg"

                capture_image(gp_context, gp_camera, filepath)

        except Exception as e:
                exit(str(e))

    else:
        print("WARNING: CAMERA-Flag is set to False")


    #waiting for user input, that everything worked the right way
    print("Press Enter to validate that Camera & Apparatus are working correctly.")

    #some input here




    time.sleep(5.0)

#-----[4] scanning material-----#
    print("Capturing...")
    print("Started: " + time.asctime(time.localtime(time.time())))

    #pre-computations and definitions
    overall_shots = compute_shots(degree)
    time_average  = 0.0 # Seconds
    time_started  = float(time.time()) # Seconds

    for current_shot in range( 1, overall_shots + 1):
        #time taking 2
        time_1 = float(round(time.time() * 1000.0))

        if not ARDUINO: time.sleep(1.5) # just simulating

        #setting current motor positions
        if(ARDUINO):

            #calculating current motor positions
            current_position = compute_position( current_shot, overall_shots, degree);

            #setting motor positions

        #taking and waiting for picture
        if(CAMERA):
            current_filepath = current_folder + "capture_" + str(current_shot) + ".raw"

            capture_image(gp_context, gp_camera, current_filepath)
        
            #validating, that picture is saved
            if not os.path.exists(current_filepath):
                exit("File not saved.")

        #time taking 2
        time_2 = float(round(time.time() * 1000.0))

        #averaging time
        if(time_average == 0.0):  #first time taking
            time_average = time_2 - time_1
        else:                   #every other case of time taking
            tmp_time_average = time_2 - time_1
            time_average = (time_average + tmp_time_average) / 2.0

        #information output
        if((current_shot % INFO_INTERVAL) == 0): #time to print some info

            passed_time = float(round(time.time() * 1000.0)) - time_started
            time_left = time_average * (overall_shots - current_shot)

            print("Average time for a picture: " + str(round(time_average)) + " Seconds")
            print("               Passed time: " + str(round(passed_time))  + " Seconds")
            print("     Left time (estimated): " + str(round(time_left))    + " Seconds")

    print("Finished: " + time.asctime(time.localtime(time.time())))

#-----[5] cleaning up-----#
    #arduino
    if(ARDUINO):
        serial_connection.close() # close port
    
    #camera
    if(CAMERA):
        gp.check_result(gp.gp_camera_exit(gp_camera, gp_context))


if __name__ == '__main__':
    main()