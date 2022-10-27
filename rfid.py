from cmath import nan
import serial
import re
myCard = ['B2736D13','700C7A73', '9158D000']
def rfid(ser):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        parse = line.split()
        if len(parse)==6:
            if parse[0] == 'Card':
                print("we get a card~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                localUID = ''.join(parse[2:6])
                flag = False
                for card in myCard:
                    if localUID == card:
                        print('u can pass')
                        ser.write(b"open\n")
                        Flag=True
                        return True
        return False
def distanceIdentification(ser):
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        #print(line)
        parse = line.split()
        if len(parse) == 3:
            if parse[0] == 'distance:':
                print("receive a distance: ", int(parse[1]))
                if int(parse[1]) < 20 and int(parse[1])>5:
                    return False
                else:
                    return True

def topSerial(ser):
    if ser.in_waiting > 0 :
        line = ser.readline().decode('utf-8').rstrip()
        #print(line)
        parse = line.split()
        parseSize = len(parse)
        if parseSize == 6:#card
            if parse[0] == 'Card':
                print("we get a card~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                localUID = ''.join(parse[2:6])
                for card in myCard:
                    if localUID == card:
                        print('u can pass')
                        ser.write(b"open\n")
                        return 'we know this card'
        elif parseSize == 3:#distance
            if parse[0] == 'distance:':
                #print("receive a distance: ", int(parse[1]))
                if int(parse[1]) < 10 and int(parse[1])>0:
                    return 'object close to the car'
                else:
                    return 'no hazard detected'
        elif parseSize == 2:#photoResistor
            if parse[0] == 'photoResister:':
                if int(parse[1]) < 15:
                    return 'too dark'
        #elif parseSize == 5:
        #elif parseSize == 5:
        #    if parse[0] == 'XYZ' and parse[1] == 
        elif parseSize > 8:
            x = int(parse[6])
            y = int(parse[7])
            z = int(parse[8])
            xyzAcc = [x,y,z]
            #('xyz: ',xyzAcc)
            if x*x+y*y+z*z > 55000:
                return 'get forced movement'
            
if __name__ == '__main__':
    print('ok~~')
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        res = topSerial(ser)
        if res :
            print(res)
    #while True:
    #    rfid(ser)
    #    distanceIdentification(ser)