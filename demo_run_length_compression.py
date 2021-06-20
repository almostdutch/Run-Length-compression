#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo_run_length_compression.py

Demo: Run-Length compression of binary images
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
import matplotlib.image as mpimg 
from run_length_compression_utils import RunLengthEncode, RunLengthDecode

# load sample image
image_original = np.array(mpimg.imread('sample_image_source.tif'));
image_original = image_original.astype(np.float32);

# generate binary image
mask_1  = image_original >= 256 / 2;
mask_0 = image_original < 256 / 2;
binary_image = image_original
binary_image[mask_1] = 1;
binary_image[mask_0] = 0;

# generate colormap
cmap = matplotlib.colors.ListedColormap(['black', 'white'])

# save binary array image
binary_image = binary_image;
# binary_image = binary_image[0:46, 0:30];
plt.imsave('sample_image_source.png', binary_image, cmap=cmap)

# image_original = binary_image;
# image_original = image_original.astype(np.uint8);

# Runlength encoding
file_source = "sample_image_source.png";
file_encoded = "sample_image_encoded";
Transpose = False;
RunLengthEncode(file_source, file_encoded, Transpose);

# Runlength decoding
file_encoded = "sample_image_encoded";
file_decoded = "sample_image_decoded.png";
RunLengthDecode(file_encoded, file_decoded);

# Load the original version
image1= np.array(mpimg.imread('sample_image_source.png'));
image1 = image1.astype(np.uint8);
image1 = image1[:, :, 0];

# Load the decoded version
image2 = np.array(mpimg.imread('sample_image_decoded.png'));
image2 = image2.astype(np.uint8);
image2 = image2[:, :, 0];

# Compare the original and decoded versions
if (image1 == image2).all():
    print('SUCCESS. The original and decoded versions are identical!');
else:
    print('FAILURE. The original and decoded versions are NOT identical!');
        
# show images: original and decoded
fig_width, fig_height = 5, 5;
fig, ((ax1, ax2)) = plt.subplots(nrows=1, ncols=2, figsize=(fig_width, fig_height));

ax1.imshow(image1, cmap='gray')
ax1.set_title("image original")
ax1.set_axis_off()

ax2.imshow(image2, cmap='gray')
ax2.set_title("image decoded")
ax2.set_axis_off()
plt.tight_layout()

