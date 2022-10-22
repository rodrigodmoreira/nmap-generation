from scipy.signal import convolve2d as conv2d
import numpy as np


def gaussian_blur(img, intensity=4):
    return conv2d(img, np.array([
            [1,2,1],
            [2,4,2],
            [1,2,1]
        ])*intensity/4,
        mode='same'
    ) / 16
