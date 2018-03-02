import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkFileDialog
from Tkinter import Tk

"""
FISH TRACKER CLASS
"""
n_rows = 2
n_columns = 3


class FishTracker(object):
    def __init__(self):
        self.mouse_x_array, self.mouse_y_array, self.fish_number_array = [], [], []
        self.current_frame = 0
        self.frame_no_array, self.fish_x, self.fish_y = [], [], []
        self.save_exp_var = True
        self.locX, self.locY = np.empty(4), np.zeros(4)
        self.video_filepath = ""
        self.window_name = ""

    def visualise_coordinates(self):
        # visualize coordinates
        self.create_figure(self.frame_no_array, self.fish_x, 'X Coordinates visualisation', 'frame number',
                           'x-coordinate (pixel)')
        self.create_figure(self.frame_no_array, self.fish_y, 'Y Coordinates visualisation', 'frame number',
                           'y-coordinate (pixel)')
        self.create_figure(self.fish_x, self.fish_y, 'X and Y Coordinates', 'y-coordinate (pixel)',
                           'x-coordinate (pixel)')
        # Block=true prevents the graphs from closing immediately
        plt.show(block=True)

    def create_figure(self, x_axis, y_axis, title, x_label, y_label):
        """
        :type x_axis: List[int]
        :type y_axis: List[int]
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
            for fish_no in range(len(self.fish_x)):
                output_file.write('{0}, {1} \n'.format(self.fish_x[fish_no], self.fish_y[fish_no]))

        output_file.close()

        # plot trajectories function

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
        ret, frame = capture.read()
        self.current_frame = frame
        # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if ret:  # check if the frame has been read properly
            fr_len = len(self.frame_no_array)

            self.display_frame_number(self.current_frame, capture)
            # clicking at fish adds a circular point - has to be outside the while loop
            cv2.setMouseCallback(self.window_name, self.draw_point)

            while fr_len == len(self.frame_no_array):
                cv2.imshow(self.window_name, self.current_frame)  # show it
                self.track_fish_through_frames(capture)

    def roi_video(self):
        height, width, ch = self.current_frame.shape
        roi_height = height / n_rows
        roi_width = width / n_columns

        images = []
        for vid_height in range(0, n_rows):
            for vid_width in range(0, n_columns):
                tmp_image = self.current_frame[
                            vid_height * roi_height: (vid_height + 1) * roi_height,
                            vid_width * roi_width:(vid_width + 1) * roi_width
                            ]
                images.append(tmp_image)

    def draw_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.current_frame, (x, y), 5, (0, 255, 0), -1)
            self.mouse_x_array.append(x)
            self.mouse_y_array.append(y)

    @staticmethod
    def display_frame_number(frame_no, capture):
        cv2.putText(frame_no, 'frame ' + str(capture.get(1)), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)

    def track_fish_through_frames(self, capture):
        if cv2.waitKey(1) % 0xFF == ord('n'):  # press n to get to next frame
            if 0 < len(self.mouse_x_array) and not [] == self.mouse_y_array[-1:]:  # check if mouse clicked
                self.frame_no_array.append(capture.get(1))
                fish_no = len(self.mouse_x_array)
                self.fish_number_array.append(fish_no)
                # add all of coordinates to the list to be printed with a new line to separate the frames
                for x in range(fish_no):
                    self.fish_x.append(self.mouse_x_array[x])
                    self.fish_y.append(self.mouse_y_array[x])
                self.fish_x.append(" ")
                self.fish_y.append(" ")
                # reset mouse coordinates
                del self.mouse_x_array[:]
                del self.mouse_y_array[:]
                # another option is self.mouse_x_array[:] = []
            else:
                cv2.putText(self.current_frame, 'Please first click on a point', (830, 130), cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255), 2)  # display the frame number

    @staticmethod
    def close_capture_window(capture):
        capture.release()
        cv2.destroyAllWindows()
