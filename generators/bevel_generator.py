from turtle import shape
from cv2 import threshold
from skimage.color import rgb2gray, rgba2rgb
import numpy as np
from scipy.ndimage import distance_transform_edt

from generator import Generator
from sobel_filter import normalized_sobel_filter, sobel_filter, sobel_gradient
from gaussian_filter import gaussian_blur

class BevelGenerator(Generator):
    def __init__(self):
        super().__init__(
            folder='D:/git/nmap-generation/assets',
            img_file='knight.png',
            normal_file_suffix='_bevel_normal'
        )


    def _apply_filters(self, img,
            normal_intensity = 1.0, # multiplier
            shape_intensity = 2.0, # multiplier
            info_intensity = 1.0, # multiplier
            gray_treshold = 0.3, # greater == more darker colors will be cut off
            sobel_treshold = 0.75, #  greater == more edges will be considered
            edt_mix=0.25 # greater == more info from color / less == more shape from silhouette
        ):
        # grayscale
        img_gray = rgb2gray(rgba2rgb(img))


        ## MASKS
        # ranges 0 ~ 1
        # alpha mask
        img_alpha_mask = np.ceil(img[:,:,3])/255.0
        self._register_img_to_plot(img_alpha_mask)

        # grayscale treshold mask
        img_gray_mask = np.clip(np.ceil(img_gray - gray_treshold), 0, 1)
        self._register_img_to_plot(img_gray_mask)

        # sobel mask
        _, sobel_mask_v, sobel_mask_h = sobel_filter(img_gray)
        img_sobel_mask = sobel_gradient(sobel_mask_v, sobel_mask_h)
        img_sobel_mask /= np.amax(img_sobel_mask)
        img_sobel_mask = np.clip(img_sobel_mask + sobel_treshold, 0, 1)
        img_sobel_mask = 1 - np.floor(img_sobel_mask)
        self._register_img_to_plot(img_sobel_mask)

        # final mask 0 ~ 1
        img_final_mask = img_alpha_mask * img_gray_mask * img_sobel_mask
        self._register_img_to_plot(img_final_mask)


        ## euclidean distance transform
        # alpha mask / grayscale mask / final mix
        img_edt_shape = self._apply_intensity(self._apply_edt(img_alpha_mask), shape_intensity)
        self._register_img_to_plot(img_edt_shape)

        img_edt_info = self._apply_intensity(self._apply_edt(img_final_mask), info_intensity)
        self._register_img_to_plot(img_edt_info)

        img_edt = img_edt_shape * (edt_mix) + img_edt_info * (1-edt_mix)
        self._register_img_to_plot(img_edt)


        # blur
        img_edt_blur = gaussian_blur(img_edt)
        self._register_img_to_plot(img_edt_blur)

        # reverse mask to get correct normal directions
        img_edt_final = 1 - img_edt_blur
        self._register_img_to_plot(img_edt_final)

        # sobel filter to generate normals
        img_sobel, _,_ = normalized_sobel_filter(img_edt_final, normal_intensity)
        self._register_img_to_plot(img_sobel)

        return img_sobel


    def _apply_edt(self, img):
        img_edt = distance_transform_edt(img)
        _max = np.amax(img_edt)
        if _max != 0:
            img_edt = (img_edt/_max) # normalize into 0 ~ 1
        return img_edt
    
    def _apply_intensity(self, img, intensity):
        return np.clip(img * intensity, 0, 1)



if __name__ == '__main__':
    BevelGenerator().run(.95)
