import RPi.GPIO as GPIO
from time import sleep
from webCam import getImg
from ypoint import getpoint
from sensor_forward import sensor_f
from sensor_right import sensor_r
import cv2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Motor():
    def __init__(self, In1A, In2A, In1B, In2B):
        self.In1A = In1A
        self.In2A = In2A
        self.In1B = In1B
        self.In2B = In2B
        GPIO.setup(self.In1A, GPIO.OUT)
        GPIO.setup(self.In2A, GPIO.OUT)
        GPIO.setup(self.In1B, GPIO.OUT)
        GPIO.setup(self.In2B, GPIO.OUT)
        self.pwmA1 = GPIO.PWM(self.In1A, 10000);
        self.pwmA2 = GPIO.PWM(self.In2A, 10000);
        self.pwmA1.start(0);
        self.pwmA2.start(0);
        self.pwmB1 = GPIO.PWM(self.In1B, 10000);
        self.pwmB2 = GPIO.PWM(self.In2B, 10000);
        self.pwmB1.start(0);
        self.pwmB2.start(0);

    def move(self, speed=0.5, turn=0, t=0):
        #print(turn)
        speed *=100
        turn *= 100
        if speed>0:
           leftSpeed = speed + turn 
           rightSpeed = speed - turn
        else:
           leftSpeed = speed - turn 
           rightSpeed = speed + turn
        if leftSpeed > 100:
            leftSpeed = 100
        elif leftSpeed < -100:
            leftSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100
        #print(f'turn: {turn}')
        print(f'left speed: {rightSpeed}, right speed: {leftSpeed}')
        #self.pwmA.ChangeDutyCycle(abs(leftSpeed))
        #self.pwmB.ChangeDutyCycle(abs(rightSpeed))

        if leftSpeed > 0:
            self.pwmA1.ChangeDutyCycle(0)
            self.pwmA2.ChangeDutyCycle(abs(leftSpeed))
        elif leftSpeed==0:
            self.pwmA1.ChangeDutyCycle(0)
            self.pwmA2.ChangeDutyCycle(0)
        else :
            self.pwmA2.ChangeDutyCycle(0)
            self.pwmA1.ChangeDutyCycle(abs(leftSpeed))

        if rightSpeed > 0:
            self.pwmB2.ChangeDutyCycle(0)
            self.pwmB1.ChangeDutyCycle(abs(rightSpeed))
        elif rightSpeed==0:
            self.pwmB1.ChangeDutyCycle(0)
            self.pwmB2.ChangeDutyCycle(0)
        else:
            self.pwmB1.ChangeDutyCycle(0)
            self.pwmB2.ChangeDutyCycle(abs(rightSpeed))
        sleep(t)
    def stopturn(self):
        print('1')
        self.move(0, -0.2, 2.1)
        

    def stop(self, t=0):
        self.pwmA1.start(0);
        self.pwmA2.start(0);
        self.pwmB1.start(0);
        self.pwmB2.start(0);
        sleep(t)


def main():
    motor.move(0.1, 0, 3)
    #motor.move(0.2, 0, 3)
    motor.stop(2)
 
    #motor.move(0.3,0,1)#turn left
  
 
            #distance_right = sensor_r(
    """motor.move(0.3,0,3)#go forward
    motor.stop(0.5)
    motor.move(0,-0.2,1.3)#turn right
    motor.stop(0.5)
    motor.move(0.3,0,3)
    motor.stop(0.5)
    motor.move(0,-0.2,1.3)
    motor.stop(1)
    motor.move(0.3,0,2)
    motor.stop(1)
    motor.move(0,0.2,1.3)"""


if __name__ == '__main__':
    motor = Motor(2, 3, 4, 17)
    while True:
        main()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break