from dronekit import *
import time
import cv2
cap = cv2.VideoCapture(0)

#connect to vehicle
vehicle = connect("127.0.0.1:14551",baud=921600,wait_ready=True)
#takeoff function
def arm_takeoff(height) :
    #check if drone is ready
    while not vehicle.is_armable :
        print("Waiting for drone.")
        time.sleep(1)
    #Change mode to Guided and arm
    print("arming")
    vehicle.mode = VehicleMode('GUIDED') #We changed the mode
    vehicle.armed = True #we're asking it to arm
    #check if the drone is armed
    while not vehicle.armed :
        print("Not yet armed")
        time.sleep(1)
    #takeoff
    print("Takeoff.")
    vehicle.simple_takeoff(height)
    #report altitude
    while True :
        print('Reached',vehicle.location.global_relative_frame.alt)
        if(vehicle.location.global_relative_frame.alt >= height*(0.95)) :
         print("Target reached.")
         break
#call takeoff functionarm_takeoff(200)
while True:
    ret,img=cap.read()#This returns a tuple in which we have , ret="Gives 1 or True if it has successfully able to get the pic from the camera.,img = gives the frame at a particular time. ,"
    res,bbox,image2 = detector.detectAndDecode(img)
    if res == '1':
        arm_takeoff(10)
        print(bbox)
        cv2.imshow('QR Code',image2)
    elif res == '2':
        print('land')
        vehicle.mode = VehicleMode('RTL')
        while True:
           print("Landing and reached :",vehicle.location.global_relative_frame.alt)
           if (vehicle.location.global_relative_frame.alt == 0)
             break
    if ret:
        cv2.imshow('video',img)
    cv2.waitKey(1)#usually,in micro seconds
#hover for 10 sec
#land
#End the connection
vehicle.close()  