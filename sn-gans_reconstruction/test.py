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
parser.add_argument('--mask', default='', type=str,
                    help='The filename of mask, value 255 indicates mask.')
parser.add_argument('--output', default='test_output/output.png', type=str,
                    help='Where to write output.')
parser.add_argument('--checkpoint_dir', default='logs/model_dir_61', type=str,
                    help='The directory of tensorflow checkpoint.')



path_img =r"E:\sih\generative_inpainting\testing_only\c____img_1_31.tif"
# path_img = "examples/try1.jpg"

output_path =path_img[:-4] +"_output_GI.tif" 
print("Gonna Start")
print(path_img) 
print(type(path_img))

def array_to_jpg_image(f):
    l=(f*(255/4095))//1
    gray=np.uint8(l)
    # im = Image.fromarray(gray)
    return gray

# path_mask = "mask_try1.jpg"

if __name__ == "__main__":
    FLAGS = ng.Config('inpaint.yml')
    print("hey")
    # ng.get_gpus(1)
    args, unknown = parser.parse_known_args()

    model = InpaintCAModel()

    # image = cv2.imread(path_img)

    image = tiff.imread(path_img)
    ratio = np.amax(image)/256
    stacked_img = np.stack((image/ratio,)*3,axis=-1)
    image =stacked_img[:,:,:]

    cv2.imwrite("test_input/input.tif",image)
    
    
    # print(image)
    # # temp_image = array_to_jpg_image(image)
    # # print(temp_image)
    
    # print("main")
    # # img = cv2.cvtColor(temp_image, cv2.COLOR_BGR2GRAY)
    # # img = cv2.cvtColor(temp_image,cv2.COLOR_GRAY2BGR)
    # ret, thresh1 = cv2.threshold(image, 130, 255, cv2.THRESH_BINARY)


    # img = thresh1
    # kernel = np.ones((3,3),np.uint8)
    # dilation = cv2.dilate(img,kernel,iterations = 2)

    # print("Increased mask")
    # ret, thresh2 = cv2.threshold(dilation, 130, 255, cv2.THRESH_BINARY)


    # cv2.imwrite("test_output/mask.JPG",thresh2)

    im_array = image
    horizontal = np.where(~im_array.any(axis = 1))[0].tolist()
    vertical = np.where(~im_array.any(axis = 0))[0].tolist()

    mask = np.zeros(shape = im_array.shape, dtype = im_array.dtype)

    print(im_array.dtype)

    for x in horizontal:
        mask[x, :] = 65535

    for y in vertical:
        mask[:, y] = 65535
        


    cv2.imwrite("test_output/mask.JPG",mask)
    print(mask)

    print(image.shape)
    print(mask.shape)
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
        # cv2.imwrite(output_path, result[0][:, :, ::-1]*ratio)
        imsave(output_path,final_array)


        print("\n\n\nOUTPUT GENERATED\n\n\n")