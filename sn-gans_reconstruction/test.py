import argparse
import sys
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import neuralgym as ng
from PIL import Image
import tifffile as tiff
from tifffile import imsave
import warnings


from inpaint_model import InpaintCAModel

warnings.filterwarnings("ignore")


print("python function called")
parser = argparse.ArgumentParser()
parser.add_argument('--image', default='', type=str,
                    help='The filename of image to be completed.')
parser.add_argument('--output', default='test_output/output.png', type=str,
                    help='Where to write output.')
parser.add_argument('--checkpoint_dir', default='logs/118', type=str,
                    help='The directory of tensorflow checkpoint.')



path_img = args.image

output_path = args.output


print("Gonna Start")
# print(path_img) 
# print(type(path_img))

def array_to_jpg_image(f):
    l=(f*(255/4095))//1
    gray=np.uint8(l)
    return gray

def mask_t(l,flag,t):
    d=l.shape
    k= np.zeros(d,dtype=np.uint8)
    if flag == 0:  
        temp=np.where(l<=t)
        k[temp]=255                                                
    elif flag == 1:        
        temp=np.where(l>=t)
        k[temp]=255
    return k

if __name__ == "__main__":
    FLAGS = ng.Config('sat_reconstruction.yml')
    print("hey")
    # ng.get_gpus(1)
    args, unknown = parser.parse_known_args()

    model = InpaintCAModel()

    image = tiff.imread(path_img)
    image1 = image
    ratio = np.amax(image)/256
    stacked_img = np.stack((image/ratio,)*3,axis=-1)
    image =stacked_img[:,:,:]

    im_array = image
    horizontal = np.where(~im_array.any(axis = 1))[0].tolist()
    vertical = np.where(~im_array.any(axis = 0))[0].tolist()

    mask = np.zeros(shape = im_array.shape, dtype = im_array.dtype)

    # print(im_array.dtype)

    for x in horizontal:
        mask[x, :] = 65535

    for y in vertical:
        mask[:, y] = 65535
        

    # print(mask)
    # print(image.shape)
    # print(mask.shape)
    # mask = cv2.resize(mask, (0,0), fx=0.5, fy=0.5)

    assert image.shape == mask.shape

    h, w, _ = image.shape
    grid = 8
    image = image[:h//grid*grid, :w//grid*grid,:]
    mask = mask[:h//grid*grid, :w//grid*grid,:]
    print('Shape of image: {}'.format(image.shape))

    image = np.expand_dims(image, 0)
    mask = np.expand_dims(mask, 0)
    input_image = np.concatenate([image, mask], axis=2)

    sess_config = tf.ConfigProto()
    sess_config.gpu_options.allow_growth = True
    with tf.Session(config=sess_config) as sess:
        input_image = tf.constant(input_image, dtype=tf.float32)
        output = model.build_server_graph(FLAGS, input_image,reuse=tf.AUTO_REUSE)
        print("Model returned")
        output = (output + 1.) * 127.5
        output = tf.reverse(output, [-1])
        output = tf.saturate_cast(output, tf.uint8)
        # load pretrained model
        vars_list = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)
        assign_ops = []
        for var in vars_list:
            vname = var.name
            from_name = vname
            var_value = tf.contrib.framework.load_variable(args.checkpoint_dir, from_name)
            assign_ops.append(tf.assign(var, var_value))
        sess.run(assign_ops)
        print('Model loaded.')
        result = sess.run(output)

        print("Gonna flush the output")
        final_array = result[0][:, :, ::-1]*ratio//1
        final_array = final_array[:,:,1]
        final_array = final_array.astype(np.uint16)
        print(final_array.shape)
        print(final_array.dtype)
        
        l = []
        l1 = image1
        l2 = final_array
        mask=mask_t(l1,0,300)
        k = np.where(mask==255)
        l=l1
        print(l,"\n",l1)
        l[k]=(l2[k])
            
        imsave(output_path,l)


        print("\n\n\nOUTPUT GENERATED\n\n\n")