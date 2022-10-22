import enum
from math import ceil
from tokenize import Number
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def show_images(images, max_row=None):
    num_images = len(images)

    fig, axes = None, None
    if max_row:
        fig, axes = plt.subplots(ncols=max_row, nrows=ceil(num_images/max_row))
    else:
        fig, axes = plt.subplots(ncols=num_images)
    axes = axes.ravel()

    for i in range(num_images):
        cmap = None
        image = images[i]

        if isinstance(images[i][1], matplotlib.colors.LinearSegmentedColormap):
            cmap = images[i][1]
            image = images[i][0]
        
        axes[i].imshow(image, cmap=cmap)
    fig.tight_layout()
    plt.show()

def overwrite_channel(a, b, ch=0):
    if np.isscalar(b[0,0]):
        a[:,:,ch] = b[:,:]
    else:
        a[:,:,ch] = b[:,:,ch]

def normalize(vec):
    norm = np.linalg.norm(vec)
    if norm > 0:
        return np.array(vec) / np.linalg.norm(vec)
    else:
        return np.array(vec)

def normalize_img(img):
    for i, row in enumerate(img):
        for j, pixel in enumerate(row):
            img[i][j] = normalize(pixel)
    return img

def rescale_0to1(img):
    _img = np.array(img)
    _min = np.amin(img)

    if _min < 0:
        _img += abs(_min)
    else:
        _img -= abs(_min)
    
    _max = np.amax(_img)
    if _max != 0:
        _img /= _max
    return _img
