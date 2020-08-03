# Usage:
#
# python3 script.py --input original.png --output modified.png
# Based on: https://github.com/mostafaGwely/Structural-Similarity-Index-SSIM-

# 1. Import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import tifffile as tiff


imageA = tiff.imread("uploads/image.tif")
imageB = tiff.imread("uploads/image2.tif")

# 4. Convert the images to grayscale
# grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
# grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# 5. Compute the Structural Similarity Index (SSIM) between the two
#    images, ensuring that the difference image is returned
# (score, diff) = compare_ssim(grayA, grayB, full=True)
(score, diff) = compare_ssim(imageA, imageB, full=True)
diff = (diff * 255).astype("uint8")

# 6. You can print only the score if you want
print("SSIM: {}".format(score))
'''
Horizontal ->
SSIM: 0.9963796631946563    

Vertical ->
SSIM: 0.9997791623683393
'''


'''
Before 
Original and Given Horizontal -> SSIM: 0.9314753871768957

Original and Given Vertical -> SSIM: 0.924211982656181

'''

