import sys
import numpy as np
import pandas as pd
import cv2

print("Output from Python") 
print("First name: " + sys.argv[1]) 
print("Last name: " + sys.argv[2])

def main():
    

    # print("start")
    # img = cv2.imread('Capture.JPG')
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ret, thresh1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    # dst = cv2.inpaint(img,thresh1,20,cv2.INPAINT_TELEA)

    # cv2.imwrite('out_pic2.jpg',dst)
    # print("working")

#start process
    if __name__ == '__main__':
        main()
