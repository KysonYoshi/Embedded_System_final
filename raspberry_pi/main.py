from motor import Motor
from lanedetect import getLaneCurve
import cv2
from webCam import getImg
from time import sleep, time
import serial
from rfid import rfid,  distanceIdentification, topSerial
import KeyPressModule as kp
#import webCam 
##################################################
motor = Motor(2, 3, 4, 17)
kp.init()
cnt=0
doorOpen = False
forcedMove = False
moveThreshold = 121
##################################################
times = 0
def main1():
    
    img = getImg(True)
            #curveVal, th= getLaneCurve(img,2, 5)
    f=0
    t=0
            #motor.move(0.1,0,2)
            #motor.stop(2)
    if kp.getKey('UP'):
        f=0.3
    elif kp.getKey('DOWN'):
        f=-0.3
    if kp.getKey('LEFT'):
                #f*=0.75
        t=-0.1
    elif kp.getKey('RIGHT'):
                #f*=0.75
        t=0.1
            
            
    motor.move(f,t,0.1)
def main2():
                
    img = getImg()
    global cnt
    curveVal, th= getLaneCurve(img,1, 6)
    #motor.move(0,0,0.1)
    #print(curveVal)
    sen = 0.004 # SENSITIVITY
    maxVAl= 0.4 # MAX SPEED
    #if curveVal>maxVAl:curveVal = maxVAl
    #if curveVal<-maxVAl: curveVal =-maxVAl
    
    if curveVal>0:
        #sen =0.005#0.43
        if curveVal<5: curveVal=0
    else:
        if curveVal>-5: curveVal=0
    #print(-curveVal*sen)
    #print(f'curveVal*sen: {curveVal*0.005}')
    #print(f"sen: {sen}")
    if th>10000:
        f=0.2
    else:
        f=0
        sen=0
        
    motor.move(f,-curveVal*sen,0.0001)
    
 
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    handmod=-1
    state=1
    lockstate=''
    lightstate=0
    while True:
        start=time()
        if kp.getKey('h') and state:
            handmod*=-1
            state=-1
            sleep(1)
        elif state<-1:
            state=1
        #objectdetected = distanceIdentification(ser)
        #stopSignal = rfid(ser)
        
        serialResult = topSerial(ser)
        if serialResult == 'get forced movement': 
            forcedMove = True
                
        if serialResult == 'object close to the car':
            motor.move(0,0,0.5)
            handmod=1
            
        if handmod>0 or forcedMove:
            main1() #hand
        else:
            main2() #auto
            
        if kp.getKey('o') or serialResult == 'we know this card':
            ser.write(b"open\n")
            lockstate='open'
        elif kp.getKey('c'):
            ser.write(b"close\n")
            lockstate='close'
            
        if kp.getKey('l'):
            ser.write(b"light\n")
            lightstate+=1
            lightstate%=2
        elif serialResult == 'too dark':
            if lightstate%2==0:
                ser.write(b"light\n")
                lightstate+=1
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            motor.move(0,0,1)
            break
        if kp.getKey('q'):
            break
        
        if kp.getKey('s'):
            forcedMove = False
        
        print(f'FPS: {1/(time()-start):.2f}, mode: {handmod}, lock: {lockstate}, light: {lightstate}, serialResult: {serialResult}')
        #print(f'{handmod}.')
    #motor.stop(2)