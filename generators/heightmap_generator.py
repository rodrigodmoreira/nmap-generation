from skimage.color import rgba2rgb, rgb2gray
import numpy as np

from generator import Generator
from sobel_filter import normalized_sobel_filter

class HeightmapGenerator(Generator):
    def __init__(self):
        super().__init__(
            folder='D:/git/nmap-generation/assets',
            img_file='knight_hm.png',
            normal_file_suffix='_heightmap_normal'
        )
    
    def _apply_filters(self, img, normal_intensity=1):
        # grayscale filter
        img_gray = rgb2gray(rgba2rgb(img))
        self._register_img_to_plot([img_gray, 'gray'])

        # normalized sobel filter
        img_sobel, img_sobel_vert, img_sobel_hor = normalized_sobel_filter(1 - img_gray, normal_intensity)
        self._register_img_to_plot(img_sobel_vert, img_sobel_hor, img_sobel)

        return img_sobel

if __name__ == '__main__':
    HeightmapGenerator().run(.9)
