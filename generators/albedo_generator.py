from skimage.color import rgb2gray, rgba2rgb
from matplotlib import pyplot as plt

from generator import Generator
from sobel_filter import normalized_sobel_filter

import numpy as np

class AlbedoGenerator(Generator):
    def __init__(self):
        super().__init__(
            folder='D:/git/nmap-generation/assets',
            img_file='knight.png',
            normal_file_suffix='_albedo_normal'
        )
    
    def _apply_filters(self, img, normal_intensity=1.0):
        # grayscale filter
        img_gray = rgb2gray(rgba2rgb(img))
        self._register_img_to_plot([img_gray, plt.cm.get_cmap('gray')])

        # normalized sobel filter
        img_sobel, img_sobel_vert, img_sobel_hor = normalized_sobel_filter(img_gray, normal_intensity)
        self._register_img_to_plot(img_sobel_vert, img_sobel_hor, img_sobel)

        return img_sobel

if __name__ == '__main__':
    AlbedoGenerator().run(.9)
