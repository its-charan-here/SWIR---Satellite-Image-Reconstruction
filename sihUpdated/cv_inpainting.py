import numpy as np
import pandas as pd
import cv2
import sys

print("starting image recovery")
img = cv2.imread("uploads/image.jpg")
print(img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

dst = cv2.inpaint(img,thresh1,20,cv2.INPAINT_TELEA)

cv2.imwrite('views/pic1.jpg',dst)
cv2.imwrite('views/pic2.jpg',img)
print("image recovery completed!")
