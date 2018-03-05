import cv2
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
        # mouse_x_list, mouse_y_list - lists to hold x and y coordinates of points that user clicked in current frame
        # fish_x, fish_y - lists to hold coordinates of all fish in all frames
        # TODO delete: fish_number_list
        self.mouse_x_list, self.mouse_y_list, self.fish_number_list = [], [], []
        self.frame_no_list, self.fish_x, self.fish_y = [], [], []
        self.fish_no_dict = {}
        self.current_frame, self.previous_frame = {}, {}
        self.video_filepath = ""
        self.window_name = "Fishies"

    # TODO FIX
    def visualise_coordinates(self):
        # visualize coordinates
        self.create_figure(self.frame_no_list, self.fish_x, 'X Coordinates visualisation', 'frame number',
                           'x-coordinate (pixel)')
        self.create_figure(self.frame_no_list, self.fish_y, 'Y Coordinates visualisation', 'frame number',
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
        output_filename = 'Outputs\\output_{0}.csv'.format(filename)
        try:
            with open(output_filename, 'w') as output_file:
                for fish_no in range(len(self.fish_x)):
                    output_file.write('{0}, {1} \n'.format(self.fish_x[fish_no], self.fish_y[fish_no]))

            output_file.close()

        except IOError as e:
            print("Unable to write to a file {0}. Writing to a new file. ({1})"
                  .format(output_filename, e))
            self.write_to_output_file(filename + '-RETRY')

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
        self.previous_frame = self.current_frame.copy()
        # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self.roi_video()

        if ret:  # check if the frame has been read properly
            fr_len = len(self.frame_no_list)

            self.display_frame_text(self.current_frame, capture)
            # clicking at fish adds a circular point - has to be outside the while loop
            cv2.setMouseCallback(self.window_name, self.draw_point)

            while fr_len == len(self.frame_no_list):
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

        # # Display the resulting sub-frame
        # for x in range(0, n_rows):
        #     for y in range(0, n_columns):
        #         cv2.imshow(str(x * n_columns + y + 1), images[x * n_columns + y])
        #         # cv2.moveWindow(str(x * n_columns + y + 1), 100 + (y * roi_width), 50 + (x * roi_height))

    def write_no_fish_to_file(self, filename):
        output_filename = 'Outputs\\fish_no_output_{0}.csv'.format(filename)
        try:
            with open('Outputs\\fish_no_output_{0}.csv'.format(filename), 'w') as output_file:
                self.print_dictionary(output_file)
            output_file.close()
        except IOError as e:
            print("Unable to write to a file '{0}'. Writing to a new file '{1}-RETRY'. ({2})"
                  .format(output_filename, filename, e))
            self.write_to_output_file(filename + '-RETRY')

    def print_dictionary(self, output_file):
        for key, value in self.fish_no_dict.items():
            if hasattr(value, '__iter__'):
                output_file.write('{0} \n'.format(key))
                self.print_dictionary(value)
            else:
                output_file.write('{0}, {1} \n'.format(key, value))

    # todo remove the point if pressed sth
    # allows removing once!!
    def draw_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.previous_frame = self.current_frame.copy()
            cv2.circle(self.current_frame, (x, y), 5, (0, 255, 0), -1)
            self.mouse_x_list.append(x)
            self.mouse_y_list.append(y)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.current_frame = self.previous_frame.copy()
            del self.mouse_x_list[-1]
            del self.mouse_y_list[-1]

    def display_frame_text(self, frame_no, capture):
        cv2.putText(frame_no, 'frame ' + str(capture.get(1)), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        cv2.putText(self.current_frame, 'Right click to undo', (830, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    def track_fish_through_frames(self, capture):
        if cv2.waitKey(1) % 0xFF == ord('n'):  # press n to get to next frame
            if 0 < len(self.mouse_x_list) and not [] == self.mouse_y_list[-1:]:  # check if mouse clicked
                self.frame_no_list.append(capture.get(1))

                # TODO CHANGE FISH_NO_list into the dictionary
                fish_no = len(self.mouse_x_list)
                self.fish_number_list.append(fish_no)

                # add all of coordinates to the list to be printed with a new line to separate the frames
                self.fish_x.extend(self.mouse_x_list)
                self.fish_y.extend(self.mouse_y_list)
                self.fish_x.append(" ")
                self.fish_y.append(" ")
                # reset mouse coordinates
                del self.mouse_x_list[:]
                del self.mouse_y_list[:]
                # another option is self.mouse_x_list[:] = []
            else:
                cv2.putText(self.current_frame, 'Please first click on a point', (830, 130), cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255), 2)  # display the frame number

    @staticmethod
    def close_capture_window(capture):
        capture.release()
        cv2.destroyAllWindows()
