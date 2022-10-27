import cv2
import numpy as np
import utlis

curveList = []
avgVal = 10
intialTrackBarVals = [60,80,20,240]
utlis.initializeTrackbars(intialTrackBarVals)

def getpoint(img, c=0):
    imgCopy = img.copy()
    imgResult = img.copy()
    ####step 1
    imgThres = utlis.thresholding(img, c)
    ####step 2
    hT,wT,c = img.shape
    #intialTrackBarVals = [0,0,0,240]
    #utlis.initializeTrackbars(intialTrackBarVals)
    points = utlis.valTrackbars()
    imgWarp = utlis.warpImg(imgThres,points,wT,hT)
    imgWarpPoints = utlis.drawPoints(imgCopy,points)

    ####step 3
    middePoint,imgHist, m = utlis.getHistogram(imgWarp,display=True,minPer=0.5,region=4)
    #print(f'{m}')
    #print(f'curveAveragePoint: {curveAveragePoint}, middePoint: {middePoint}')

    return m
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    #intialTrackBarVals = [60,80,20,214]
    #utlis.initializeTrackbars(intialTrackBarVals)
    while True:
        success, img = cap.read()
        img = cv2.resize(img,(480,240))
        curve =getpoint(img, 0)
        print(curve)

        #cv2.imshow('vid',img)
        cv2.waitKey(1)