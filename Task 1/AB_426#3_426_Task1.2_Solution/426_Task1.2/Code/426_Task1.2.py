# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  E-Yantra Robotics Competition
*                  ================================
*  This software is intended to check version compatiability of open source software
*  Theme: ANT BOT
*  MODULE: Task1.2
*  Filename: Task1.2.py
*  Version: 1.0.0  
*  Date: October 31, 2018
*  
*  Author: e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""

"""
ArUco ID Dictionaries: 4X4 = 4-bit pixel, 4X4_50 = 50 combinations of a 4-bit pixel image
List of Dictionaries in OpenCV's ArUco library:
DICT_4X4_50	 
DICT_4X4_100	 
DICT_4X4_250	 
DICT_4X4_1000	 
DICT_5X5_50	 
DICT_5X5_100	 
DICT_5X5_250	 
DICT_5X5_1000	 
DICT_6X6_50	 
DICT_6X6_100	 
DICT_6X6_250	 
DICT_6X6_1000	 
DICT_7X7_50	 
DICT_7X7_100	 
DICT_7X7_250	 
DICT_7X7_1000	 
DICT_ARUCO_ORIGINAL

Reference: http://hackage.haskell.org/package/opencv-extra-0.2.0.1/docs/OpenCV-Extra-ArUco.html
Reference: https://docs.opencv.org/3.4.2/d9/d6a/group__aruco.html#gaf5d7e909fe8ff2ad2108e354669ecd17
"""

import numpy as np
import cv2
import cv2.aruco as aruco
import math
import sys
import csv
#import aruco_lib as arl


#Dictionary TO BE EDITED BY THE USER for the shapes to be deteccted and marked.
#Format is 'Image_no': [('Color 1', 'Shape 1'), ('Color 2', 'Shape 2'), (aruco.DICT_nXn_Combinations)]
#If no shape is to be detected, enter 'none' as shown in example Image2
#Minimum 1 and Maximum 2 shapes are detected and marked.

detect = {
    'Image1': [('green', 'triangle'), ('blue', 'circle'), (aruco.DICT_4X4_100)],
    'Image2': [('red', 'square'), ('none', 'none'), (aruco.DICT_4X4_100)],
    'Image3': [('green', 'circle'), ('red', 'triangle'), (aruco.DICT_5X5_1000)],
    'Image4': [('blue', 'triangle'), ('blue', 'square'), (aruco.DICT_5X5_1000)],
    'Image5': [('red', 'circle'), ('green', 'square'), (aruco.DICT_7X7_250)]
   #<Image_Name> : [(,), (,), (aruco.DICT_)] 
    }

#Error Detection for 2 shapes of the same colour is done in the code that follows.
#Error detection for both the shapes being none is done in the code that follows.

i = 1
arucoID = 0
begin = 1

#function for writing required data to the .csv file
def writeCsv(data):
    global begin
    if (begin):
        with open('426_Task1.2.csv', mode='w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(data)
        begin = 0
    else:
        with open('426_Task1.2.csv', mode='a', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(data)

#helper function
def dict_id():
    global i
    im_idl = 'Image'+str(i)
    dictID = detect[im_idl][2]
    return dictID

def aruco_detect(path_to_image):
    global i
    global arucoID
    '''
    you will need to modify the ArUco library's API using the dictionary in it to the respective
    one from the list above in the aruco_lib.py. This API's line is the only line of code you are
    allowed to modify in aruco_lib.py!!!
    '''
    #The AruCo marker's angle and the ID is not modified to be of the same color as the one shown-
    #in the example diagram as we were directed to not modify the aruco_lib.py. Kindly keep it in considerarion.
    
    img = cv2.imread(path_to_image)     #give the name of the image with the complete path
    id_aruco_trace = 0
    det_aruco_list = {}

    up_black = np.array([10, 10, 10])
    low_black = np.array([0, 0, 0])
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    maskblack = cv2.inRange(hsv,low_black,up_black)
    _, contours_black, _ = cv2.findContours(maskblack, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    det_aruco_list = detect_Aruco(img)
    arucoID = list(det_aruco_list.keys())[0]
    color_detect(img)
    if det_aruco_list:
        img3 = mark_Aruco(img,det_aruco_list)
        id_aruco_trace = calculate_Robot_State(img3,det_aruco_list)
        #print(id_aruco_trace)        
        cv2.imshow('image',img)
        cv2.waitKey(0)

    cv2.imwrite('ArUco'+str(i)+'.jpg',img)     #For writing the output image.
    i = i+1
    cv2.destroyAllWindows()

def color_detect(img):
    '''
    code for color Image processing to detect the color and shape of the 2 objects at max.
    mentioned in the Task_Description document. Save the resulting images with the shape
    and color detected highlighted by boundary mentioned in the Task_Description document.
    The resulting image should be saved as a jpg. The boundary should be of 25 pixels wide.
    '''
    cv2.imshow('Color_Detect', img)
    global arucoID
    im_id = 'Image'+str(i)
    
    #ERROR Detection: Both the to-be-detected shapes are none. Violation of minimum 1 object criterion. 
    if detect[im_id][0][0] == 'none':
        if detect[im_id][0] == detect[im_id][1]:
            print('ERROR! Both shapes are none. Violation of the rule that minimum 1 shape should be present for detection.')
        
    
    # Setting limits for masking of different colors
    low_blue = np.array([100,100,100])
    up_blue = np.array([120,255,255])
    low_green = np.array([45,100,100])
    up_green = np.array([70,255,255])
    low_red = np.array([0,50,50])
    up_red = np.array([8,255,255])
    low_red1 = np.array([170,50,50])
    up_red1 = np.array([180,255,255])

    #Dictionary to keep a track of the color of the contours to be drawn. 
    Contclr = {                     
            'blue': (0, 0, 255),
            'red': (0, 255, 0),
            'green': (255, 0, 0)
            }

    #Identification of Shape based on the number of corners.
    def shape (n, app):
            if (n==3):
                    return "triangle"
            elif (n==4):
                    (s1, s2, s3, s4) = cv2.boundingRect(app)
                    ratio = s3/ float(s4)
                    if(ratio>=0.95 and ratio<=1.05):
                            return "square"
                    else:
                            return "rectangle"
            elif (n==5):
                    return "pentagon"
            else:
                    return "circle"

    #Identification of Color using masking.
    #shape_list.append("test"+str(i)+".jpg")
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    maskblue = cv2.inRange(hsv,low_blue,up_blue)
    _, contours_blue, _ = cv2.findContours(maskblue, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    maskgreen = cv2.inRange(hsv,low_green,up_green)
    _, contours_green, _ = cv2.findContours(maskgreen, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    maskred1 = cv2.inRange(hsv,low_red,up_red)
    maskred2 = cv2.inRange(hsv,low_red1,up_red1)
    maskred = maskred1 + maskred2
    _, contours_red, _ = cv2.findContours(maskred, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #dictionary to hold the contours for referencing.
    Contlist = {			
            'blue':contours_blue,
            'green':contours_green,
            'red':contours_red
    }

    '''
    for j in Contlist:
            cv2.drawContours(img,Contlist[j],-1,(0,0,0),2)
    cv2.imshow('Contours', img)
    '''
    data = ['ArUco'+str(i)+'.jpg', arucoID, '', '']
    for j in Contlist:
            flag = 0
            
            #ERROR DETECTION: To detect if 2 shapes of same color exists in the input image. Violation.
            count = {
                    'square': 0,
                    'triangle': 0,
                    'circle': 0,
                    'ellipse': 0
                    }
            
            for c in Contlist[j]:
                    txt = []
                    app = cv2.approxPolyDP(c,0.04*cv2.arcLength(c,True),True)
                    x = len(app)
                    if (j == 'blue'):
                            txt = ('blue', shape(x,app))
                    elif (j == 'green'):
                            txt = ('green', shape(x,app))
                    elif (j == 'red'):
                            txt = ('red', shape(x,app))

                    if txt[1] == 'circle':
                            x1, y1, w1, h1 = cv2.boundingRect(c)
                            #cv2.rectangle(img, (x1,y1), (x1+w1, y1+h1), (150, 150, 200), 2)
                            ratio1 = w1/h1
                            if(ratio1 <= 0.95 or ratio1>=1.05):
                                    #print('Changing')
                                    txt = (txt[0], 'ellipse')       #Differentiating between an ellipse and a circle with a TOLERABILITY OF 0.5%

                    count[txt[1]] = count[txt[1]] + 1
                    if(count[txt[1]] == 2):
                            flag = 1
                            break       #If 2 shapes are of the same color, then post an ERROR message and break.
                        
                    #print(count)
                    #print(txt)
                    for ite in range(len(detect[im_id])):
                        if detect[im_id][ite] == txt:
                            M = cv2.moments(c)
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            #data[2+ite] = '('+str(cx)+','+str(cy)+')'
                            data[2+ite] = (cx, cy)
                            shapeClr = img[cy][cx]
                            cv2.drawContours(img,[c],-1,Contclr[j],50)
                            cv2.drawContours(img,[c],-1,(int(shapeClr[0]), int(shapeClr[1]), int(shapeClr[2])),-1)
                            cv2.putText(img,'('+str(cx)+','+str(cy)+')',(cx-50,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)
                    '''if txt in detect[im_id]:
                            #print('Matched')    #Checking for the correct shapes according to the dictionary.
                            cv2.drawContours(img,c,-1,Contclr[txt[0]],25)
                            M = cv2.moments(c)  #Finding centre of mass.
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            centre = [(cx, cy)]
                            #print(centre[0])
                            cv2.putText(img,str(centre[0]),(cx-50,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),2)'''
                    '''        
                    cv2.imshow('Loop', img)
                    cv2.waitKey(0)
                    '''
                                
            if flag == 1:
                    print("ERROR! Two shapes of the same colour found. Terminating and moving on to the next image.")
                    break

    #cv2.imshow("ColorImage",result_image)
    if flag != 1:
        writeCsv(data)
    else:
        data = ['ArUco'+str(i)+'.jpg', arucoID, '', ''] 
        writeCsv(data)
############################################################################################################################################################
############################################################################################################################################################
    ### THE LIBRARY aruco_lib.py STARTS HERE. NOTHING HAS BEEN ALTERED IN THIS EXCEPT THE DICT COMBINATION. ###
'''
functions in this file:
* angle_calculate(pt1,pt2, trigger = 0) - function to return angle between two points
* detect_Aruco(img) - returns the detected aruco list dictionary with id: corners
* mark_Aruco(img, aruco_list) - function to mark the centre and display the id
* calculate_Robot_State(img,aruco_list) - gives the state of the bot (centre(x), centre(y), angle)
'''

def angle_calculate(pt1,pt2, trigger = 0):  # function which returns angle between two points in the range of 0-359
    angle_list_1 = list(range(359,0,-1))
    #angle_list_1 = angle_list_1[90:] + angle_list_1[:90]
    angle_list_2 = list(range(359,0,-1))
    angle_list_2 = angle_list_2[-90:] + angle_list_2[:-90]
    x=pt2[0]-pt1[0] # unpacking tuple
    y=pt2[1]-pt1[1]
    angle=int(math.degrees(math.atan2(y,x))) #takes 2 points nad give angle with respect to horizontal axis in range(-180,180)
    if trigger == 0:
        angle = angle_list_2[angle]
    else:
        angle = angle_list_1[angle]
    return int(angle)

def detect_Aruco(img):  #returns the detected aruco list dictionary with id: corners
    aruco_list = {}
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(dict_id())#aruco.Dictionary_get(aruco.DICT_4X4_50)   #creating aruco_dict with 5x5 bits with max 250 ids..so ids ranges from 0-249
    print(aruco_dict)
    parameters = aruco.DetectorParameters_create()  #refer opencv page for clarification
    #lists of ids and the corners beloning to each id
    print(parameters)
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters = parameters)
    #corners is the list of corners(numpy array) of the detected markers. For each marker, its four corners are returned in their original order (which is clockwise starting with top left). So, the first corner is the top left corner, followed by the top right, bottom right and bottom left.
    # print len(corners), corners, ids
    print(corners)
    print(len(corners))
    gray = aruco.drawDetectedMarkers(gray, corners,ids)
    # cv2.imshow('frame',gray)
    #print (type(corners[0]))
    if len(corners):    #returns no of arucos
        #print (len(corners))
        #print (len(ids))
        for k in range(len(corners)):
            temp_1 = corners[k]
            temp_1 = temp_1[0]
            temp_2 = ids[k]
            temp_2 = temp_2[0]
            aruco_list[temp_2] = temp_1
        return aruco_list

def mark_Aruco(img, aruco_list):    #function to mark the centre and display the id
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in key_list:
        dict_entry = aruco_list[key]    #dict_entry is a numpy array with shape (4,2)
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]#so being numpy array, addition is not list addition
        centre[:] = [int(x / 4) for x in centre]    #finding the centre
        #print centre
        orient_centre = centre + [0.0,5.0]
        #print orient_centre
        centre = tuple(centre)  
        orient_centre = tuple((dict_entry[0]+dict_entry[1])/2)
        #print centre
        #print orient_centre
        cv2.circle(img,centre,1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[0]),1,(0,0,255),8)
        cv2.circle(img,tuple(dict_entry[1]),1,(0,255,0),8)
        cv2.circle(img,tuple(dict_entry[2]),1,(255,0,0),8)
        cv2.circle(img,orient_centre,1,(0,0,255),8)
        cv2.line(img,centre,orient_centre,(255,0,0),4) #marking the centre of aruco
        cv2.putText(img, str(key), (int(centre[0] + 20), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA) # displaying the idno
    return img

def calculate_Robot_State(img,aruco_list):  #gives the state of the bot (centre(x), centre(y), angle)
    robot_state = {}
    key_list = aruco_list.keys()
    font = cv2.FONT_HERSHEY_SIMPLEX

    for key in key_list:
        dict_entry = aruco_list[key]
        pt1 , pt2 = tuple(dict_entry[0]) , tuple(dict_entry[1])
        centre = dict_entry[0] + dict_entry[1] + dict_entry[2] + dict_entry[3]
        centre[:] = [int(x / 4) for x in centre]
        centre = tuple(centre)
        #print centre
        angle = angle_calculate(pt1, pt2)
        cv2.putText(img, str(angle), (int(centre[0] - 80), int(centre[1])), font, 1, (0,0,255), 2, cv2.LINE_AA)
        robot_state[key] = (int(centre[0]), int(centre[1]), angle)#HOWEVER IF YOU ARE SCALING IMAGE AND ALL...THEN BETTER INVERT X AND Y...COZ THEN ONLY THE RATIO BECOMES SAME
    #print (robot_state)

    return robot_state
    
'''
det_aruco_list = {}
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    det_aruco_list=detect_Aruco(frame)
    img = mark_Aruco(frame,det_aruco_list)
    robot_state=calculate_Robot_State(img,det_aruco_list)
    print robot_state

    cv2.imshow('image',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
'''
                             ### The library aruco_lib.py ENDS here. ###
############################################################################################################################################################
############################################################################################################################################################


if __name__ == "__main__":
    writeCsv(['Image Name', 'ArUco ID', '(x,y) Object-1', '(x,y) Object-2'])
    for j in range(1,len(detect)+1):
        img_name = 'Image'+str(i)+'.jpg'
        aruco_detect(img_name)






