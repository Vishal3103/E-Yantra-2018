'''
* Team Id : 426
* Author List : Rohan Katkan, Joshua D'Cunha, Vishal Sinha, Nayan Nair
* Filename: TaskA
* Theme: Ant Bot
* Functions: detect_markers(img),readFromNano()
* Global Variables: None


Function: detect_markers(img)
Arguments: img -> image file captured by the PiCam
Outputs: List of ArUco IDs detected in the image file
Purpose: To detect the SIMs on the eYRC arena

'''

import cv2                      #for image processing
import cv2.aruco as aruco       #for detecting ArUco IDs
import serial                   #for communicating with the Arduino Nano
import csv                      #for creating and filling the .csv file
from picamera import PiCamera   #for controlling the PiCam
from time import sleep          #for introducing required delays


def detect_markers(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #load aruco_dictionary to assign aruco_id after image loading and marker detection
    aruco_dict = aruco.Dictionary_get(aruco.DICT_7X7_1000)
    parameters = aruco.DetectorParameters_create()

    #getting aruco_image corners and aruco_id
    corners, aruco_id, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)

    if (len(aruco_id) == 0):
        return [[-1]]
    
    return aruco_id

'''
Function: readFromNano()
Arguments: None
Outputs: Byte recevied from Arduino Nano
Purpose: To wait for bytes sent from Arduino Nano
'''

def readFromNano():
    ans = ser.read()
    while (str(ans) == "b''"):
        ans = ser.read()
    return ans

if __name__ == "__main__":

    print("Starting Task A")

    #creates instance of PiCamera class to control the PiCam
    camera = PiCamera()

    #(re)creates .csv file with name eYRC#AB#426.csv
    with open('eYRC#AB#426.csv', mode='w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')

    #creates instance of Serial class for Arduino-Pi communication
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(b'1')
    ans = readFromNano()

    #loop to capture images of SIM on arena, detect ArUco IDs present, and write them to the .csv file
    for simNo in [1, 2, 3, 0]:
        ser.write(b'1')
        ans = readFromNano()
        fileName = 'SIM_'+str(simNo)+'.jpg'
        camera.capture(fileName)
        sleep(2)
        img = cv2.imread(fileName)
        aruco_id = detect_markers(img)
        print("SIM Detected! ID -> ", aruco_id[0][0])
        with open('eYRC#AB#426.csv', mode='w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            data = ['SIM '+simNo, aruco_id[0][0]]
            writer.writerow(data)
        
        

