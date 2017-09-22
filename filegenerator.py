# -*- coding: utf-8 -*-

import os

#command list
ARDUINO = "Gcode"   + " "
CAMERA  = "Picture" + " "

def main():

    #directory organization
    current_directory = os.getcwd()

    if not os.path.exists(current_directory + "/gcodescripts"):
        print("Creating gcode output folder...")
        os.makedirs(current_directory + "/gcodescripts/")

    resolution = 90
    filename = "./gcodescripts/"+str(resolution)+"_degrees_scan.gcode"
    file = open( filename,'w')
    deltaZ = 66.66*(resolution/9)
    deltaOthers = 5*(resolution/9)

    xStart = 25
    yStart = 3
    zStart = 168

    xPos = xStart
    yPos = yStart
    zPos = zStart

    xMax = 105
    yMax = 53
    zMax = 835

    xDegree=resolution
    yDegree=90
    zDegree=0
    eDegree=0

    print("Creating gcode file: " + filename)

    while(zPos <= zMax):
        file.write(ARDUINO + "G1 Z"+str(int(zPos))+ " F4000 S1\n")
        file.write(ARDUINO + "M400\n") # wait until all moves are finished
        zPos = zPos + deltaZ
        while(yPos <= yMax):
            file.write(ARDUINO + "G1 Y"+str(int(yPos))+ " F500 S1\n")
            file.write(ARDUINO + "M400\n") # wait until all moves are finished
            yPos = yPos + deltaOthers
            while(xPos <= xMax):
                file.write(ARDUINO + "G1 X"+str(int(xPos))+ " F1500 S1\n")
                file.write(ARDUINO + "M400\n") # wait until all moves are finished
                xPos = xPos + deltaOthers
                for aE in range(0,40/(resolution/9),1):
                    file.write(CAMERA  + "E-"+str(eDegree)+"_X-"+str(xDegree)+"_Y-"+str(yDegree)+"_Z-"+str(zDegree)+"\n")
                    file.write(ARDUINO + "G91\n") #relative coordinates
                    file.write(ARDUINO + "G1 E"+str(int(5*(resolution/9)))+ " F3000 S1\n")
                    file.write(ARDUINO + "G4 P"+str(2000)+"\n") #wait a second
                    file.write(ARDUINO + "G90\n") #absolute coordinates
                    file.write(ARDUINO + "M400\n") # wait until all moves are finished
                    eDegree+=resolution
                xDegree+=resolution
                eDegree=18

            xPos = xStart
            file.write(ARDUINO + "G28 X\n")
            file.write(ARDUINO + "G1 X"+str(int(xPos))+ " F1500 S1\n")
            file.write(ARDUINO + "M400\n") # wait until all moves are finished
            yDegree-=resolution
            xDegree=0

        yPos = yStart
        file.write(ARDUINO + "G28 Y\n")
        file.write(ARDUINO + "G1 Y"+str(int(yPos))+ " F1500 S1\n")
        file.write(ARDUINO + "M400\n") # wait until all moves are finished
        zDegree+=resolution
        yDegree=90

    file.write(ARDUINO + "G28")

    file.close()

if __name__ == '__main__':
    main()