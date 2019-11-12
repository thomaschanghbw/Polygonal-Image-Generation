import matplotlib.pyplot as plt

import numpy as np

class Display:
    def __init__(self, target_im):
        self.fig = plt.figure()
        # self.imshow = plt.imshow(np.asarray(target_im))

        # self.fig, self.ax = plt.subplots(1, 1)
        # self.imshow = self.ax.imshow(np.asarray(target_im))

        plt.axis('off')
        plt.ion()
        self.imshow = plt.imshow(np.asarray(target_im))
        plt.show()
        plt.pause(0.0001)

    def show(self, im, text):
        self.fig.suptitle(text)
        # x = plt.imshow(np.asarray(im))
        self.imshow.set_data(np.asarray(im))
        # self.fig.canvas.draw_idle()
        plt.draw()
        plt.pause(0.0001)

