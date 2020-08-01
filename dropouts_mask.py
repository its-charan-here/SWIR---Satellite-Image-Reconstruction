from PIL import Image
import numpy as np
import sys
#where any

infile = sys.argv[1]

if len(sys.argv) == 3:
	extension = sys.argv[2]
else:
	extension = "png"

im = Image.open(infile)

im_array = np.asarray(im)

horizontal = np.where(~im_array.any(axis = 1))[0].tolist()
vertical = np.where(~im_array.any(axis = 0))[0].tolist()

mask = np.zeros(shape = im_array.shape, dtype = im_array.dtype)

print(im_array.dtype)

for x in horizontal:
	mask[x, :] = 65535

for y in vertical:
	mask[:, y] = 65535
	
mask_im = Image.fromarray(mask)



mask_im.save(infile[:-4] + "_dropoutmask." + extension)


#print(im_array)