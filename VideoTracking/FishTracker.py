import numpy as np
import matplotlib.pyplot as plt
import tkFileDialog
from Tkinter import Tk

"""
FISH TRACKER CLASS
"""


class FishTracker (object):
    def __init__(self):
        # initialize global variables
        self.mX, self.mY = -1, -1
        self.fr, self.fishX, self.fishY = [], [], []
        self.save_exp_var = True
        self.locX, self.locY = np.empty(4), np.zeros(4)
        self.video_filepath = ""

    def visualise_coordinates(self):
        # visualize coordinates
        self.create_figure(self.fr, self.fishX, 'X Coordinates visualisation', 'frame number', 'x-coordinate (pixel)')
        self.create_figure(self.fr, self.fishY, 'Y Coordinates visualisation', 'frame number', 'y-coordinate (pixel)')
        self.create_figure(self.fishX, self.fishY, 'X and Y Coordinates', 'y-coordinate (pixel)', 'x-coordinate (pixel)')
        # Block=true prevents the graphs from closing immediately
        plt.show(block=True)

    def create_figure(self, x_axis, y_axis, title, x_label, y_label):
        """
        :type x_axis: int
        :type y_axis: int
        :type title: str
        :type x_label: str
        :type y_label: str
        """
        if self.is_not_string(title) or self.is_not_string(x_label) or self.is_not_string(y_label):
            raise TypeError("Title or labels not strings. Wrong type.")
        plt.figure()
        plt.plot(x_axis, y_axis, 'k')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    @staticmethod
    def is_not_string(string):
        # type: (str) -> bool
        return type(string) is not str

    def write_to_output_file(self, filename):
        """
        :type filename: str
        """
        with open('Outputs\\output_{0}.csv'.format(filename), 'w') as output_file:
            for n in range(len(self.fr)):
                output_file.write("{0}, {1}, {2} \n".format(self.fr[n], self.fishX[n], self.fishY[n]))
        output_file.close()

    def get_video_file(self):
        # hides the Tk window
        root = Tk()
        root.withdraw()
        # ask for video file
        while not self.video_filepath:
            # restrict to only videos
            self.video_filepath = tkFileDialog.askopenfilename(title="Choose a video file",
                                                    filetypes=[("Video Files", "*.avi *.mp4")])


