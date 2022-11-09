import cv2 #Import a Computer Vision library
cap = cv2.VideoCapture(0)#This is used for capturing the video.(0 represents that its from 1st camera.)
detector = cv2.QRCodeDetector()
while True:
    ret,img=cap.read()#This returns a tuple in which we have , ret="Gives 1 or True if it has successfully able to get the pic from the camera.,img = gives the frame at a particular time. ,"
    res,bbox,image2 = detector.detectAndDecode(img)
    if res:
        print(res)
        print(bbox)
        cv2.imshow('QR Code',image2)
    if ret:
        cv2.imshow('video',img)
    cv2.waitKey(1)

