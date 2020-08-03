#python driver.py --image "<input file" --output "<output file name"
import argparse
import numpy as np
import tifffile as tiff
from tifffile import imsave
from PIL import Image
import cv2
from test import inpainting_sat , load_model
model = load_model()

parser = argparse.ArgumentParser()
parser.add_argument('--image', default='', type=str,
                    help='The filename of image to be completed.')
parser.add_argument('--output', default='output.tif', type=str,
                    help='Where to write output.')
args, unknown = parser.parse_known_args()


in_path = args.image
out_path = args.output

input_img = tiff.imread(in_path)

img_shape = input_img.shape

#splitting
master_arr = []
for i in range(img_shape[1]//256):
    temp_arr = []
    for j in range(img_shape[0]//256):
        x=256*j
        y=256*i
        k=input_img[x:x+256,y:y+256]
        temp_arr.append(k)
    master_arr.append(temp_arr)


# applying
for i in range(len(master_arr)):
    for j in range(len(master_arr[i])):
        master_arr[i][j] = inpainting_sat(master_arr[i][j],model)
        print(i,j)

fin =[]
#joining
for  i in range(len(master_arr)):
    temp = master_arr[i][0]
    for j in range(len(master_arr[i])-1):
        temp = np.vstack((temp,master_arr[i][j+1]))
    fin.append(temp)

final  = fin[0]
for i in range(len(fin)-1):
    final = np.hstack((final,fin[i+1]))
np.array(final).shape


imsave(out_path,final)