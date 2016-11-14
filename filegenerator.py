# -*- coding: utf-8 -*-

import os

def main():

    #directory organization
    current_directory = os.getcwd()

    if not os.path.exists(current_directory + "/gcodescripts"):
        print("Creating gcode output folder...")
        os.makedirs(current_directory + "/gcodescripts/")

    resolution = 18
    filename = "./gcodescripts/"+str(resolution)+"_degrees_scan.gcode"
    file = open( filename,'w')
    deltaZ = 66.66*(resolution/9)
    deltaOthers = 5*(resolution/9)

    startx = 25
    starty = 3
    startz = 168

    xPos = startx
    yPos = starty
    zPos = startz

    maxx = 105
    maxy = 53
    maxz = 835

    xDegree=resolution
    yDegree=90
    zDegree=0
    eDegree=0

    pictureDelay = 1500 #delay in ms

    print("Creating gcode file: " + filename)

    while(zPos <= maxz):
        file.write("Command G1 Z"+str(int(zPos))+ " F4000 S1\n")
        file.write("Command M400\n") # wait until all moves are finished
        zPos = zPos + deltaZ
        while(yPos <= maxy):
            file.write("Command G1 Y"+str(int(yPos))+ " F500 S1\n")
            file.write("Command M400\n") # wait until all moves are finished
            yPos = yPos + deltaOthers
            while(xPos <= maxx):
                file.write("Command G1 X"+str(int(xPos))+ " F1500 S1\n")
                file.write("Command M400\n") # wait until all moves are finished
                xPos = xPos + deltaOthers
                for aE in range(0,40/(resolution/9),1):
                    file.write("Picture " + "E-"+str(eDegree)+"_X-"+str(xDegree)+"_Y-"+str(yDegree)+"_Z-"+str(zDegree)+".jpg\n")
                    file.write("Command G4 P"+str(pictureDelay)+"\n") #wait a second
                    file.write("Command G91\n") #relative coordinates
                    file.write("Command G1 E"+str(int(5*(resolution/9)))+ " F3000 S1\n")
                    file.write("Command G4 P"+str(2000)+"\n") #wait a second
                    file.write("Command G90\n") #absolute coordinates
                    file.write("Command M400\n") # wait until all moves are finished
                    eDegree+=resolution
                xDegree+=resolution
                eDegree=18

            xPos = startx
            file.write("Command G28 X\n")
            file.write("Command G1 X"+str(int(xPos))+ " F1500 S1\n")
            file.write("Command M400\n") # wait until all moves are finished
            yDegree-=resolution
            xDegree=0

        yPos = starty
        file.write("Command G28 Y\n")
        file.write("Command G1 Y"+str(int(yPos))+ " F1500 S1\n")
        file.write("Command M400\n") # wait until all moves are finished
        zDegree+=resolution
        yDegree=90

    file.write("G28\n")

    file.close()

if __name__ == '__main__':
    main()