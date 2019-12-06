import io
from PIL import ImageTk
from tkinter import *

import numpy as np

class Display:
    @staticmethod
    def get_display(should_show_display, target_im):
        if should_show_display:
            return EnabledDisplay(target_im)
        else:
            return DummyDisplay(target_im)

    def __init__(self, target_im):
        pass

    def show(self, im, text):
        pass

class EnabledDisplay(Display):
    def __init__(self, target_im):
        # self.fig = plt.figure()
        #
        # plt.axis('off')
        # plt.ion()
        # self.imshow = plt.imshow(np.asarray(target_im))
        # plt.show()
        # plt.pause(0.0001)

        self.root = Tk()
        self.root.title("Polygon algorithm")

        self.root.geometry('1000x1000')

        self.lbl = Label(self.root, text="Starting...")

        self.lbl.pack(side = BOTTOM)

        self.original_img = ImageTk.PhotoImage(target_im)
        self.original_image = Label(self.root, image=self.original_img)
        self.original_image.pack(side = LEFT)

        self.displayed_img = ImageTk.PhotoImage(target_im)
        self.image = Label(self.root, image=self.displayed_img)
        self.image.pack(side = LEFT)

        self.root.update_idletasks()
        self.root.update()

    def show(self, im, text):
        # self.fig.suptitle(text)
        # # x = plt.imshow(np.asarray(im))
        # self.imshow.set_data(np.asarray(im))
        # # self.fig.canvas.draw_idle()
        # plt.draw()
        # plt.pause(0.0001)

        # event, values = self.window.read()
        # self.window['_OUTPUT_'].update(text)
        # self.window['_IMAGE_'].update(self._getImageFromPIL(im))

        self.lbl.configure(text=text)
        self.displayed_img = ImageTk.PhotoImage(im)
        self.image.configure(image=self.displayed_img)
        self.root.update_idletasks()
        self.root.update()

class DummyDisplay(Display):
    pass