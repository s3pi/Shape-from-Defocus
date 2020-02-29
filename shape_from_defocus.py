import cv2
import os
import matplotlib.image as mpimg 
import matplotlib.pyplot as plt 
from sklearn.feature_extraction.image import extract_patches_2d
import numpy as np
import math
from PIL import Image
import time

def extract_patches_from_file(file_path):
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    window_shape = (patch_width,patch_height)
    patches_each_img = extract_patches_2d(img,window_shape)

    return patches_each_img

def V1_all_patches_all_imgs(): 
    # with open(log_file_path, 'a') as log_file:
    #     log_file.write("Extracting patches.....\n")

    # Extract all patches of all images and store in RAM (Memory intensive)
    patches_all = []
    for file in os.listdir(data_path):
        file_path = os.path.join(data_path,file) 
        patches_each_img = extract_patches_from_file(file_path)
        patches_all.append(patches_each_img)

    #shape(patches_all) = (num_imgs, num_patches_per_img, patch_width, patch_height)
    result = np.zeros((img_width, img_height), dtype=np.uint8)

    for mm in range (0, num_patches_per_img):
        maxi = 0
        for img_num in range(0, num_imgs):
            patches_of_img = patches_all[img_num]
            var = np.var(patches_of_img[mm])
            if var > maxi:
                maxi = var
                selected_file = img_num
        # Store the central pixel value of the patch from selected img
        patches_of_img = patches_all[selected_file]
        selected_patch = patches_of_img[mm]
        center = selected_patch[math.floor(patch_width/2)][math.floor(patch_height/2)]
        x_cood = mm // (img_height - patch_height + 1)
        y_cood = mm % (img_height - patch_height + 1)
        result[x_cood][y_cood] = center

    img = Image.fromarray(result)
    img.save(str(img_width) + 'by' + str(img_height) + '_' + str(patch_width) + 'by' + str(patch_height) + '_Img.png')

def list_all_files():
    all_imgs = []
    for file in os.listdir(data_path):
        img = cv2.imread(os.path.join(data_path, file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        all_imgs.append(img)

    return all_imgs

def V2_one_patch_all_imgs():
    all_imgs = list_all_files()
    result = np.zeros((num_patches_x, num_patches_y), dtype=np.uint8)

    for i in range(num_patches_x):
        for j in range(num_patches_y):
            patches_var_all_imgs = []
            for each_img in all_imgs:
                patches_var_all_imgs.append(np.var(each_img[i:i+patch_width,j:j+patch_height]))
            patches_var_all_imgs = np.asarray(patches_var_all_imgs)
            # Although np.asarray() does out of place copy. Used because no argmax fun for python list.
            # Less memory but very time intensive.
            max_var_index = np.argmax(patches_var_all_imgs)

        elapsed_time = time.time() - start_time
        # with open(log_file_path, 'a') as log_file:
        #     log_file.write("Elapsed time is " + str(elapsed_time) + "\n")
        print(elapsed_time)
                
    img = Image.fromarray(result)
    img.save(str(img_width) + 'by' + str(img_height) + '_' + str(patch_width) + 'by' + str(patch_height) + '_Img.png')

def find_center(arr):
    arr_len = arr.shape[0]
    return arr[arr_len//2]

def V3_all_patches_one_img():
    files = os.listdir(data_path)
    # 1st file outside the loop
    file = files[0]
    img = cv2.imread(os.path.join(data_path, file))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    patches_each_img = extract_patches_2d(img, (patch_width, patch_height))
    patches_each_img = patches_each_img.reshape(patches_each_img.shape[0], patch_width * patch_height)

    result_prev = np.apply_along_axis(find_center, 1, patches_each_img)  
    patches_var_prev = np.var(patches_each_img, axis=1)

    #rest of the files inside the loop
    for file in files[1:]:
        img = cv2.imread(os.path.join(data_path,file))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        patches_each_img = extract_patches_2d(img,(patch_width, patch_height))
        patches_each_img = patches_each_img.reshape(patches_each_img.shape[0], patch_width * patch_height)

        result = np.apply_along_axis(find_center, 1, patches_each_img)
        patches_var = np.var(patches_each_img, axis=1)

        indicate_change = patches_var - patches_var_prev
        indices = np.where(indicate_change < 0)
        
        # Change only those values which are smaller. 
        result[indices] = result_prev[indices]
        patches_var[indices] = patches_var_prev[indices]

        result_prev = result
        patches_var_prev = patches_var
        
        # elapsed_time = time.time() - start_time
        # with open(log_file_path, 'a') as log_file:
        #     log_file.write("Elapsed time is " + str(elapsed_time) + "\n")

    img = Image.fromarray(result.reshape(num_patches_x, num_patches_y))
    img.save(str(img_width) + 'by' + str(img_height) + '_' + str(patch_width) + 'by' + str(patch_height) + '_Img.png')

#---------------------------------------------------------------------------------------------
# log_file_path = "/home/s18001/wd/Preethi/shape_from_defocus/Code/1000_by_1500/cv2_extract_patch/patch_of_patch/log_file.txt"
# with open(log_file_path, 'a') as log_file:
#     log_file.write("-----------------------------------------\nProgram Starts\n")
start_time = time.time()
data_path = '/Users/3pi/Documents/tag_sir_work/numbers_256_256'

img_width=256
img_height=256
patch_width=15
patch_height=15

assert (img_width >= patch_width) and (img_height >= patch_height) == True

num_imgs = 10
num_patches_x = img_width - patch_width + 1
num_patches_y = img_height - patch_height + 1
num_patches_per_img = num_patches_x * num_patches_y


V1_all_patches_all_imgs()
elapsed_time = time.time() - start_time
# with open(log_file_path, 'a') as log_file:
#     log_file.write("Elapsed time is " + str(elapsed_time) + "\n")





