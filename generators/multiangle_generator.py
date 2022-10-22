from tkinter import image_names
from skimage.io import imread
from skimage.color import rgba2rgb, rgb2gray
import numpy as np

from generator import Generator
from utils import rescale_0to1, show_images

class MultiangleGenerator(Generator):
    def __init__(self):
        super().__init__(
            folder='D:/git/nmap-generation/assets/4ilum',
            img_file='knight.png',
            normal_file_suffix='_multiangle_normal'
        )
        
    
    def _load_imgs(self):
        f_name, f_ext = self.IMG_FILE.split('.')

        _format = lambda suff : f'{f_name}_{suff}.{f_ext}'

        input_file_names = {
            'up': _format('up'),
            'down': _format('down'),
            'left': _format('left'),
            'right': _format('right')
        }
        input_files = {}
        for k, input_name in input_file_names.items():
            input_files[k] = imread(f'{self.FOLDER}/{input_name}')
        return input_files
    
    def _apply_filters(self, imgs, normal_intensity=1):
        in_shape = imgs['up'].shape
        out_shape = (in_shape[0], in_shape[1], 3)

        imgs_gray = {}
        for k, img in imgs.items():
            # remove alpha
            if img.shape[2] == 3:
                imgs_gray[k] = rgb2gray(img)
            else:
                imgs_gray[k] = rgb2gray(rgba2rgb(img))
            self._register_img_to_plot([img, 'gray'])

        # above-green | left-red
        img_al = np.zeros(out_shape)
        img_al[:,:,1] = self._rescale_channel(imgs_gray['up'], 0, 0.5)
        img_al[:,:,0] = self._rescale_channel(imgs_gray['left'], 0, 0.5)
        img_al = -1 * img_al + 0.5
        self._register_img_to_plot(img_al)

        # below-green | right-red
        img_br = np.zeros(out_shape)
        img_br[:,:,1] = self._rescale_channel(imgs_gray['down'], 0.51, 1)
        img_br[:,:,0] = self._rescale_channel(imgs_gray['right'], 0.51, 1)
        self._register_img_to_plot(img_br)

        # overlay blend
        output_img = np.zeros(out_shape)
        for i in range(img_al.shape[0]):
            for j in range(img_al.shape[1]):
                upper_layer_px = img_br[i,j]
                lower_layer_px = img_al[i,j]
                if np.sum(upper_layer_px)/3.0 < 0.5:
                    output_img[i,j] = 2 * lower_layer_px * upper_layer_px
                else:
                    output_img[i,j] =   1 - 2 * (1 - lower_layer_px) * (1 - upper_layer_px)
        self._register_img_to_plot(np.copy(output_img))

        # revert green channel to fix normal direction
        output_img[:,:,1] = 1 - output_img[:,:,1]

        # set blue channel
        output_img[:,:,2] = 0.9
        self._register_img_to_plot(output_img)

        return output_img
    
    def _rescale_channel(self, img, min, max):
        img_01 = rescale_0to1(img)
        return img_01 * (max - min) + min

    
    def run(self, normal_intensity = 0.5):
        imgs = self._load_imgs()

        img_normal = self._apply_filters(
            imgs=imgs,
            normal_intensity=np.clip(1 - normal_intensity, 0,1)
        )

        show_images(self._imgs_to_plot, max_row=2)

        self._save_img(img_normal)

        print(f'{self.FOLDER}/{self.IMG_FILE} {self.FOLDER}/{self.NORMAL_FILE}')
        self._run_renderer()

if __name__ == '__main__':
    MultiangleGenerator().run(.9)
