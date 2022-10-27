#!/usr/bin/env python3
import serial
import re
myCard = ['B2736D13','700C7A73']
def cardIdentification(parse):
    if len(parse)==6:
                if parse[0] == 'Card':
                    print("we get a card")
                    localUID = ''.join(parse[2:6])
                    flag = False
                    for card in myCard:
                        if localUID == card:
                            print('u can pass')
                            Flag=True
                    print('meet'+localUID)
def distanceIdentification(parse):
    if len(parse) == 3:
        if parse[0] == 'distance:':
            print("receive a distance: ", int(parse[1]))
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    print(1)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            parse = line.split()
            cardIdentification(parse)
            distanceIdentification(parse)