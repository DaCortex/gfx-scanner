# -*- coding: utf-8 -*-

import sys        #basic
import argparse   #parsing arguments
import logging    #basic logging
import datetime   #identification of files
import time       #taking time for averaging a shot
import serial     #connection to arduino
import subprocess #controlling camera

#testing
import random




#----- UTILITY METHODS -----#

#prints error message and quits the program
def error(message):
    
    sys.stderr.write("[Error] " + message)

    logging.info('Exiting program')
    sys.exit(1)

#returns current time for identification
def id():
    now = datetime.datetime.now() 

    now_str = ""
    now_str += "_y:" + str(now.year)
    now_str += "_m:" + str(now.month)
    now_str += "_d:" + str(now.day)
    now_str += "_h:" + str(now.hour)
    now_str += "_m:" + str(now.minute)

    return now_str




#----- FLAGS -----#
#for basic testing when there is no real system attatched
SANDBOX = True

#print info after x pictures
INFO_INTERVAL = 10



#----- GLOBAL VARIABLES -----#

#logger
LOG_FILENAME = 'scanner' + id() + '.log'




#----- METHODS -----#

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



#-----[1] basic input validation-----#

    parser.add_argument("degree", help="scan is executed with given degrees", type=int)

    args = parser.parse_args()

    #1: degree
    degree = args.degree
    if(360%degree != 0):
        error("Degree must be integer divider of 360° (Used: " + str(degree) + ")")


#-----[2] connecting to arduino-----#
    if(not SANDBOX):
        try:
            serial_connection = serial.Serial('/dev/ttyUSB0')  # open serial port
        except Exception, e:
            error(str(e))

        #maybe another try catch block for this one
        serial_connection.write(b'hello')     # write a string


#-----[3] connecting to camera-----#
    #subprocess!
    try:
        #subprocess.call(['ls', '-1'], shell=True) #just for testing
        subprocess.call(['gphoto2', '--capture-image'], shell=True) #just for testing
    except Exception, e:
        exit(str(e))

#-----[4] testing all components-----#
    #scanning apparatus

    #waiting for user input, that everything moved the right way

    #camera

    #waiting for user input, that the picture is o.k.


#-----[5] scanning material-----#
    #pre-computations and definitions
    overall_shots = compute_shots(degree)
    average_time = 0 # milliseconds+
    tmp_average_time = 0 # milliseconds
    passed_time = 0  # milliseconds
    left_time = 0    # milliseconds

    for current_shot in range( 1, overall_shots +1):
        #time taking 2
        time_1 = int(round(time.time() * 1000))


        #calculating current motor positions
        current_position = compute_position( current_shot, overall_shots, degree);

        #setting current motor positions
        time.sleep(1.5)

        #taking and waiting for picture
        current_filename = "image" + id() + ".raw"

        #validating, that picture is saved



        #time taking 2
        time_2 = int(round(time.time() * 1000))

        #averaging time
        if(average_time == 0):  #first time taking
            average_time = time_2 - time_1
        else:                   #every other case of time taking
            tmp_average_time = time_2 - time_1
            average_time = (average_time + tmp_average_time) / 2

        #information output
        if((current_shot % INFO_INTERVAL) == 0): #time to print some info

            left_time = average_time * (overall_shots - current_shot)

            print("Average time for a picture: " + str(average_time) + " Milliseconds")
            print("               Passed time: " + str(passed_time/1000)  +  " Seconds")
            print("     Left time (estimated): " + str(left_time/1000)    + " Seconds")

        passed_time += average_time


#-----[6] cleaning up-----#
    #arduino
    if(not SANDBOX):
        serial_connection.close() # close port


if __name__ == '__main__':
    main()