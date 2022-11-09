#import libraries
from dronekit import *
import time
import math

#connect to vehicle
vehicle = connect('127.0.0.1:14551',baud=921600,wait_ready=True)

#takeoff function
def arm_takeoff(height):
    #check if drone is ready
    while not vehicle.is_armable:
        print("Waiting for drone")
        time.sleep(1)

    #change mode and arm
    print("Arming")
    vehicle.mode=VehicleMode('GUIDED')
    vehicle.armed=True
    
    #check if drone is armed
    while not vehicle.armed:
        print("Waiting for arm\n")
        time.sleep(1)

    #takeoff
    print("Taking off")
    vehicle.simple_takeoff(height)

    #report values back every 1s and finally break out
    while True:
        print('Reached ',vehicle.location.global_relative_frame.alt)
        if(vehicle.location.global_relative_frame.alt>=height*0.95):
            print("Reached Target Altitude\n")
            break
        time.sleep(1)

def get_location_metres(original_location, dNorth, dEast):

    earth_radius = 6378137.0 #Radius of "spherical" earth
    #Coordinate offsets in radians
    dLat = dNorth/earth_radius
    dLon = dEast/(earth_radius*math.cos(math.pi*original_location.lat/180))

    #New position in decimal degrees
    newlat = original_location.lat + (dLat * 180/math.pi)
    newlon = original_location.lon + (dLon * 180/math.pi)
    if type(original_location) is LocationGlobal:
        targetlocation=LocationGlobal(newlat, newlon,original_location.alt)
    elif type(original_location) is LocationGlobalRelative:
        targetlocation=LocationGlobalRelative(newlat, newlon,original_location.alt)
    else:
        raise Exception("Invalid Location object passed")
        
    return targetlocation;#This contains latitude , longitude and altitude

def get_distance_metres(aLocation1, aLocation2):

    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5#THESE NUMBERS CONVERT IT INTO METRES

def goto(dNorth, dEast, gotoFunction=vehicle.simple_goto):

    currentLocation = vehicle.location.global_relative_frame
    targetLocation = get_location_metres(currentLocation, dNorth, dEast)
    targetDistance = get_distance_metres(currentLocation, targetLocation)
    gotoFunction(targetLocation)
    
    while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
        print("Distance to target: ", remainingDistance)
        if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print("Reached target\n")
            break;
        time.sleep(2)

#takeoff
arm_takeoff(10)

#move 100m North and 200m East
print('Moving to target location')
goto(100,200)

#landing
print('Landing')
vehicle.mode=VehicleMode('RTL')
time.sleep(20)

#close vehicle
print('Done')
vehicle.close()