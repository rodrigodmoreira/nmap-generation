from skimage.io import imread, imsave
import matplotlib.pyplot as plt
import numpy as np
import os

from utils import show_images

GODOT_EXECUTABLE = 'Godot_v3.5.1-stable_win64.exe'
REPOSITORY_PATH = 'D:/github/nmap-generation'

class Generator:
    def __init__(self,
            folder='D:/git/nmap-generation/assets',
            img_file='knight.png',
            normal_file_suffix='_normal'):
        
        self.FOLDER = folder
        self.IMG_FILE = img_file
        self.IMG_NAME, self.IMG_EXT = self.IMG_FILE.split('.')
        self.NORMAL_FILE = f'{self.IMG_NAME}{normal_file_suffix}.{self.IMG_EXT}'
        self._imgs_to_plot = []
    
    def _register_img_to_plot(self, *args):
        for arg in args:
            if isinstance(arg[1], str) and arg[1] == 'gray':
                self._imgs_to_plot.append([arg[0], plt.cm.get_cmap('gray')])
            elif len(np.array(arg).shape) == 2: # default single channel to gray
                self._imgs_to_plot.append([arg, plt.cm.get_cmap('gray')])
            else:
                self._imgs_to_plot.append(arg)
                
    
    # ----- STAGES ----- to be overridden
    def _load_img(self):
        return imread(f'{self.FOLDER}/{self.IMG_FILE}')

    def _apply_filters(self, img, normal_intensity=1.0):
        self._register_img_to_plot(img)
        return img
    
    def _save_img(self, img_normal):
        imsave(f'{self.FOLDER}/{self.NORMAL_FILE}', img_normal)
    
    def _run_renderer(self):
        # run godot renderer
        print('skipping renderer')
        return # TODO: Fix Scene not running
        cmdline_str = f'{GODOT_EXECUTABLE} --path {REPOSITORY_PATH}/renderer {REPOSITORY_PATH}/renderer/renderer3d/Renderer3D.tscn {self.FOLDER}/{self.IMG_FILE} {self.FOLDER}/{self.NORMAL_FILE}'
        print(cmdline_str)
        os.system(cmdline_str)


    # ----- RUN -----
    def run(self, normal_intensity = 0.5):
        """
            Parameters:
                normal_instensity (float): 0 ... 1
        """
        img = self._load_img()

        img_normal = self._apply_filters(
            img=img,
            normal_intensity=np.clip(1 - normal_intensity, 0,1)
        )

        show_images(self._imgs_to_plot, max_row=2)

        self._save_img(img_normal)

        self._run_renderer()

if __name__ == '__main__':
    Generator().run()
