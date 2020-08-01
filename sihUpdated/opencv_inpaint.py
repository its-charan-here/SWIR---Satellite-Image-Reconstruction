# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import timeit
from os.path import isfile, join
from PIL import Image, ImageChops 
import timeit
start = timeit.default_timer()

print("Import Done, reading the input file!")

# %%
def jpg_image_to_array(image_path):
    with Image.open(image_path) as image:         
        im_arr = np.fromstring(image.tobytes(), dtype=np.uint8)
        rgb = im_arr.reshape((image.size[1], image.size[0], 3))
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray

def array_to_jpg_image(f,d):
    dt =np.dtype(np.uint16)
    l= np.fromfile(f, dtype=dt).reshape(d)
    l=(l*(255/4095))//1
    gray=np.uint8(l)
    im = Image.fromarray(gray)
    return im


# %%

# img =array_to_jpg_image("data/white.rl0",(8238,6000))
img =Image.open("uploads/image.jpg")

# %%
a= img.size[1]
b = a//100
b


# %%
i = 0
mega_list=[]
for i in range(0,a,b): 
    # print(i)   i = 8235
    if i+b>img.size[1] :
        cropped_image = img.crop((0,i,img.size[0],a))
        # cropped_image.save('crop/pic_'+str(i)+".jpg")
        mega_list.append(cropped_image)
        break
    else:
        cropped_image = img.crop((0,i,img.size[0],i+b))
        mega_list.append(cropped_image)
    


# %%
mega_list[1]


# %%
i=0

for i in range(len(mega_list)):

    image1 = mega_list[i].convert("RGB")
    image1 = np.array(image1)
    
    img = cv2.cvtColor(image1, cv2.COLOR_RGB2GRAY) 
    ret, thresh1 = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)
    
    # kernel = np.ones((3,3),np.uint8)
    # dilation = cv2.dilate(thresh1,kernel,iterations = 1)
    # ret, thresh2 = cv2.threshold(dilation, 125, 255, cv2.THRESH_BINARY)
    

    dst = cv2.inpaint(img,thresh1,30,cv2.INPAINT_TELEA)
    if i == 0 :
        im_total = dst
    else: 
        im_total = cv2.vconcat([im_total,dst])

    i=i+1
    print("Done with : ",i,"/",str(len(mega_list)))


# %%
# im_total


# %%
# plt.imshow(cv2.cvtColor(im_total, cv2.COLOR_BGR2RGB))
plt.imsave("views/opencv_generated.jpg",cv2.cvtColor(im_total, cv2.COLOR_BGR2RGB))

stop = timeit.default_timer()
print('Time: ', stop - start)

