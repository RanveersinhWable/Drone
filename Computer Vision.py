import cv2 #Import a Computer Vision library
cap = cv2.VideoCapture(0)#This is used for capturing the video.(0 represents that its from 1st camera.)
while True:
    ret,img=cap.read()#This returns a tuple in which we have , ret="Gives 1 or True if it has successfully able to get the pic from the camera.,img = gives the frame at a particular time. ,"
    if ret:
         cv2.imshow('video',img)#This shows the 
    cv2.waitKey(1)
