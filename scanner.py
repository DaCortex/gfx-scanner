# -*- coding: utf-8 -*-

import sys        #basic
import argparse   #parsing arguments
import logging    #basic logging
import datetime   #identification of files
import serial     #connection to arduino
import subprocess #controlling camera

#-----[0] basic setup-----#
#global variables

#basic
NO_ARDUINO_CONNECTED = True
serial_connection = None

#time
now = datetime.datetime.now()

now_str = ""
now_str += "_y:" + str(now.year)
now_str += "_m:" + str(now.month)
now_str += "_d:" + str(now.day)
now_str += "_h:" + str(now.hour)
now_str += "_m:" + str(now.minute)

#logger
file_name = 'scanner' + now_str + '.log'

logging.basicConfig(filename=file_name, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.info('Program started')

#argument parser
parser = argparse.ArgumentParser()

#prints error message and quits the program
def error(message):
    logging.warning('- Error message:')

    message = "-- " + message

    logging.warning(message)
    
    sys.stderr.write("[Runtime Error] See " + file_name + " for further information.")

    logging.info('Exiting program')
    sys.exit(1)

#returns the amount of shots that need to be taken
def compute_shots(degree):
    
    #positions per variable
    light       = 180 / degree
    first_axis  = 360 / degree
    second_axis = 360 / degree

    #compute all  possible positions
    shots = light * first_axis * second_axis

    return shots

def compute_time(shots):
    time_per_shot = 2 #Seconds
    return  shots * time_per_shot

#returns the position of all motors given by the
def compute_position( shot, degree):
    
    return 5

def main():
#-----[0] basic setup-----#

    #see line 10

#-----[1] basic input validation-----#
    logging.info('Parsing arguments...')

    parser.add_argument("degree", help="scan is executed with given degrees", type=int)

    args = parser.parse_args()

    #1: degree
    degree = args.degree
    if(360%degree != 0):
        error("Degree must be integer divider of 360° (Used: " + str(degree) + ")")

    logging.info('Parsing successful')

#-----[2] connecting to arduino-----#
    logging.info('Connecting to arduino...')

    if(not NO_ARDUINO_CONNECTED):
        try:
            serial_connection = serial.Serial('/dev/ttyUSB0')  # open serial port
        except Exception, e:
            logging.info('- Unable to connect to arduino')
            error(str(e))

        logging.info('Connection with: ' + serial_connection.name)

        #maybe another try catch block for this one
        serial_connection.write(b'hello')     # write a string

    logging.info('Connection established')

#-----[3] connecting to camera-----#
    logging.info('Connecting to camera...')
    
    #subprocess!
    try:
        subprocess.call(['ls', '-1'], shell=True)
    except Exception, e:
        exit(str(e))

    logging.info('Connection established')

#-----[4] testing all components-----#
    logging.info('Testing compontents...')
    
    #scanning apparatus

    #waiting for user input, that everything moved the right way

    #camera

    #waiting for user input, that the picture is o.k.

    logging.info('Testing successful')

#-----[5] scanning material-----#
    #pre-computations
    shots = compute_shots(degree)
    time = compute_time(shots)

    logging.info('Scanning information')
    logging.info('- Degree: '           + str(degree) + '°')
    logging.info('- Overall shots: '    + str(shots))
    logging.info('- Time estimation: '  + str(time)  + ' seconds')

    logging.info('Scanning material')


    #scanning apparatus

    #camera

    logging.info('Scanning done')

#-----[6] cleaning up-----#
    #arduino
    if(not NO_ARDUINO_CONNECTED):
        serial_connection.close() # close port

    logging.info('Program ended')

if __name__ == '__main__':
    main()