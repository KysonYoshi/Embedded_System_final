import cv2
from time import time


cap = cv2.VideoCapture(0)


def getImg(display=False, size=[160, 120]):
    success, img = cap.read()
    
    img = cv2.resize(img, (size[0], size[1]))
    if display:
        cv2.imshow('IMGuu', img)
    return img


if __name__ == '__main__':
    while True:
        start=time()
        img = getImg(True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        print(f'FPS: {1/(time()-start):.2f}')