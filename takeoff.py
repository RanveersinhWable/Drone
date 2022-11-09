#import libraries
from dronekit import *
import time
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
#call takeoff function
arm_takeoff(200)
#hover for 10 sec
time.sleep(10)
#land
vehicle.mode = VehicleMode('RTL')
while True:
    print("Landing and reached :",vehicle.location.global_relative_frame.alt)
    if (vehicle.location.global_relative_frame.alt == 0)
     break
#End the connection
vehicle.close()  