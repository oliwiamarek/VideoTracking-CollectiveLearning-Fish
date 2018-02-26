import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkFileDialog
from Tkinter import Tk

"""
FISH TRACKER CLASS
"""


class FishTracker(object):
    def __init__(self):
        self.mouse_x, self.mouse_y = -1, -1
        self.frame_no = 0
        self.frame_no_array, self.fish_x, self.fish_y = [], [], []
        self.save_exp_var = True
        self.locX, self.locY = np.empty(4), np.zeros(4)
        self.video_filepath = ""
        self.window_name = ""

    def visualise_coordinates(self):
        # visualize coordinates
        self.create_figure(self.frame_no_array, self.fish_x, 'X Coordinates visualisation', 'frame number', 'x-coordinate (pixel)')
        self.create_figure(self.frame_no_array, self.fish_y, 'Y Coordinates visualisation', 'frame number', 'y-coordinate (pixel)')
        self.create_figure(self.fish_x, self.fish_y, 'X and Y Coordinates', 'y-coordinate (pixel)',
                           'x-coordinate (pixel)')
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
        Write digitized coordinates into an output file
        :type filename: str
        """
        with open('Outputs\\output_{0}.csv'.format(filename), 'w') as output_file:
            for n in range(len(self.frame_no_array)):
                output_file.write("{0}, {1}, {2} \n".format(self.frame_no_array[n], self.fish_x[n], self.fish_y[n]))
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

    def create_record_window(self):
        self.window_name = 'Fishies'
        # normalize size of the window to every screen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def track_fish(self, capture):
        # read next frame
        ret, self.frame_no = capture.read()

        if ret:  # check if the frame has been read properly
            fr_len = len(self.frame_no_array)

            self.display_frame_number(self.frame_no, capture)
            # clicking at fish adds a circular point - has to be outside the while loop
            cv2.setMouseCallback(self.window_name, self.draw_point)

            while fr_len == len(self.frame_no_array):
                cv2.imshow(self.window_name, self.frame_no)  # show it
                self.track_fish_through_frames(capture)

    def draw_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.frame_no, (x, y), 5, (0, 255, 0), -1)
            self.mouse_x, self.mouse_y = x, y

    @staticmethod
    def display_frame_number(frame_no, capture):
        cv2.putText(frame_no, 'frame ' + str(capture.get(1)), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

    def track_fish_through_frames(self, capture):
        if cv2.waitKey(1) % 0xFF == ord('n'):  # press n to get to next frame
            if -1 < self.mouse_x and -1 < self.mouse_y:  # check if mouse clicked
                self.frame_no_array.append(capture.get(1))
                self.fish_x.append(self.mouse_x)
                self.fish_y.append(self.mouse_y)
                self.mouse_x, self.mouse_y = -1, -1  # reset mouse coordinates
            else:
                cv2.putText(self.frame_no, 'Please first click on a point', (830, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)  # display the frame number

    @staticmethod
    def close_capture_window(capture):
        capture.release()
        cv2.destroyAllWindows()
