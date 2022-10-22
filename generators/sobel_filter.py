from utils import overwrite_channel, normalize_img, rescale_0to1
import numpy as np
from scipy.signal import convolve2d as conv2d 

def merge_gradients(sobel_v, sobel_h, intensity=1.0):
    out_height, out_width = sobel_v.shape
    sobel = np.full((out_height, out_width, 3), intensity, dtype=np.float64)    # b = intensity
    overwrite_channel(sobel, sobel_h / 2, 0)                                    # r = vertical
    overwrite_channel(sobel, sobel_v / 2, 1)                                    # g = horizontal
    return rescale_0to1(
        normalize_img(sobel)
    )

def partial_gradients(img_grayscale):
    sobel_operator_vert = -np.array([[1,  2,  1],
                                    [0,  0,  0],
                                    [-1,-2, -1]])
    img_sobel_vert = conv2d(img_grayscale, sobel_operator_vert, mode='same')/2

    sobel_operator_hor = np.array([[1,0,-1],
                                   [2,0,-2],
                                   [1,0,-1]])
    img_sobel_hor = conv2d(img_grayscale, sobel_operator_hor, mode='same')/2

    return img_sobel_vert, img_sobel_hor

def sobel_filter(img_grayscale, intensity=1.0):
    """
        Returns:
            tuple:
                img_merged_sobel: range 0 .. 1
    """

    img_sobel_vert, img_sobel_hor = partial_gradients(img_grayscale)
    img_merged_sobel = merge_gradients(img_sobel_vert, img_sobel_hor, intensity)

    return img_merged_sobel, img_sobel_vert, img_sobel_hor

def normalized_sobel_filter(img_grayscale, intensity=1.0):
    """
        Returns:
            tuple:
                img_merged_sobel: range 0 .. 1
    """
    img_sobel_vert, img_sobel_hor = partial_gradients(img_grayscale)
    img_merged_sobel = merge_gradients(img_sobel_vert, img_sobel_hor, intensity)

    return img_merged_sobel, img_sobel_vert, img_sobel_hor

def sobel_gradient(img_sobel_v, img_sobel_h):
    return np.sqrt(np.power(img_sobel_v, 2) + np.power(img_sobel_h, 2))
