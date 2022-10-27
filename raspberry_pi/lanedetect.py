import cv2
import numpy as np
import utlis
import time

curveList = []
avgVal = 10
intialTrackBarVals = [20,40,0,120]
utlis.initializeTrackbars(intialTrackBarVals)

def getLaneCurve(img,display=1,c=6):
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
    curveAveragePoint, imgHist, m = utlis.getHistogram(imgWarp, display=True, minPer=0.9)
    #print(f'curveAveragePoint: {curveAveragePoint}, middePoint: {middePoint}')
    curveRaw = curveAveragePoint - wT/2
    #print(f'{middePoint}, {m}, {curveRaw}')

    ####step 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))
    #print(curve)
    ####step 5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 100
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt', imgResult)

    ####normalization
    curve = curve
    if curve > 1:  curve == 1
    if curve <-1:  curve ==-1

    #cv2.imshow('thres',imgThres)
    #cv2.imshow('warp', imgWarp)
    #cv2.imshow('warpPoint', imgWarpPoints)
    #cv2.imshow('Histogram',imgHist)
    return curve, m


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    #intialTrackBarVals = [60,80,20,214]
    #utlis.initializeTrackbars(intialTrackBarVals)
    while True:
        start=time.time()
        success, img = cap.read()
        img = cv2.resize(img,(160,120))
        cv2.imshow('IMGuu', img)
        curve =getLaneCurve(img,display=2)
        #print(curve)

        #cv2.imshow('vid',img)
        cv2.waitKey(1)
        print(f'FPS: {1/(time.time()-start)}')
