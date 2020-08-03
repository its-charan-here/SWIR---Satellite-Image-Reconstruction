import cv2
import numpy as np
import tifffile as tiff
from tifffile import imsave
from PIL import Image
print("Enter")
img = tiff.imread("uploads/image2.tif")
print("read image")
def array_to_jpg_image(f):
    l=(f*(255/4095))//1
    gray=np.uint8(l)
    im = Image.fromarray(gray)
    return im
print("function done")
img_in = array_to_jpg_image(img)
img_in.save("views/input_image2.jpg")
print("output done")