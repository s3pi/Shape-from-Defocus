### Reconstruct an all-focused image from several de-focused images

Reconstruct all focused image from several defocused images.

3 versions of experiments and their corresponding results are mentioned below:

V1: Extract all the patches from all images and then apply the algorithm.
So, RAM stores data of shape: (num_of_imgs, num_of_patches, patch_size, patch_size, 1)
For example, on 1000x1500 with 51x51 patch: (10, 1377500, 51, 51, 1)
Number of I/O operations: 10
RAM required: 10 x 1377500 x 51 x 51 (35 GB)

V2: Extract all the patches from one image and apply algorithm. So, RAM at any given time will contain data of shape: (1, num_of_patches, patch_size, patch_size, 1)
For example, on 1000x1500 with 51x51 patch: (1, 1377500, 51, 51, 1)
Number of I/O operations: 10
RAM required: 1377500 x 51 x 51 (3GB)

V3: Extract one patch from all images and apply algorithm.
So, RAM at any given time will contain data of shape: 
(num_of_images, patch_size, patch_size, 1)
For example, on 1000x1500 with 51x51 patch: (10, 51, 51, 1)
Number of I/O operations: 51076
RAM required: 10 x 51 x 51 (26 KB)

In V1 and V2, inbuilt cv2 function to extract patches is used. Its highly optimized and extraction is an O(1) operation. In V3, extraction is manually done using for loop and slicing operation (saves on memory but because of too many I/O operations highly time consuming).

Img size: 1000x1500
using V1:
51x51 patch: 457 secs (7.6 mins)
91x91 patch: Inconsistent

using V2:
51x51 patch_size: 350 secs (5.8 mins)
91x91 patch_size: 8.9 hours

using V3:
51x51 patch_size: 89 hours

Img size: 4000x6000
using V1: RAM is limited. Does not work

using V2: RAM is limited. Does not work

using V3:  Will consistently work but
350x350 patch_size: 2302 days (6.3 years :P:D)

