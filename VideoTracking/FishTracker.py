import cv2
import matplotlib.pyplot as plt
import tkFileDialog
from Tkinter import Tk

"""
FISH TRACKER CLASS
https://introlab.github.io/find-object/s
http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher
"""
n_rows = 2
n_columns = 3


def return_array(array, start, element_no):
    return array[start::element_no]


class FishTracker(object):
    def __init__(self):
        # mouse_x_list, mouse_y_list - lists to hold x and y coordinates of points that user clicked in current frame
        # fish_x, fish_y - lists to hold coordinates of all fish in all frames
        # TODO delete: fish_number_list
        self.current_frame_fish_coord, self.all_fish_x_coord, self.all_fish_y_coord = [], [], []
        self.roi_fish_count, self.frame_no_list = [], []
        self.current_frame, self.previous_frame = {}, {}
        self.video_filepath = ""
        self.window_name = "Fishies"
        self.frame_no = 0
        self.roi_mid_width, self.roi_first_height, self.roi_second_height = 0, 0, 0

    @staticmethod
    def close_capture_window(capture):
        capture.release()
        cv2.destroyAllWindows()

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
        no_fish = len(self.current_frame_fish_coord)
        for x in xrange(no_fish):
            plt.plot(return_array(y_axis, x, no_fish + 1), return_array(x_axis, x, no_fish + 1))
        # plt.plot(return_array(x_axis, 1, no_fish), return_array(y_axis, 1, no_fish))
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    def create_record_window(self):
        self.window_name = 'Fishies'
        # normalize size of the window to every screen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def display_frame_text(self, frame, capture):
        self.frame_no = capture.get(1)
        cv2.putText(frame, 'frame ' + str(self.frame_no), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        cv2.putText(self.current_frame, 'Right click to undo', (830, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # allows removing once!!
    def draw_point(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.previous_frame = self.current_frame.copy()
            cv2.circle(self.current_frame, (x, y), 5, (0, 255, 0), -1)
            self.current_frame_fish_coord.append('{0}, {1}'.format(x, y))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.current_frame = self.previous_frame.copy()
            del self.current_frame_fish_coord[-1]

    def get_no_fish_for_ROI(self):
        roi = [0, 0, 0, 0, 0, 0]
        for fish in self.current_frame_fish_coord:
            coordinates = [int(x.strip()) for x in fish.split(',')]
            x = coordinates[0]
            y = coordinates[1]
            self.all_fish_x_coord.append(x)
            self.all_fish_y_coord.append(y)
            if y < self.roi_mid_width and x < self.roi_first_height:
                roi[0] += 1
            elif y < self.roi_mid_width and x < self.roi_second_height:
                roi[1] += 1
            elif y < self.roi_mid_width and x > self.roi_second_height:
                roi[2] += 1
            elif y > self.roi_mid_width and x < self.roi_first_height:
                roi[3] += 1
            elif y > self.roi_mid_width and x < self.roi_second_height:
                roi[4] += 1
            elif y > self.roi_mid_width and x > self.roi_second_height:
                roi[5] += 1
        self.all_fish_x_coord.append("")
        self.all_fish_y_coord.append("")
        return roi

    def get_video_file(self):
        # hides the Tk window
        root = Tk()
        root.withdraw()
        # ask for video file
        while not self.video_filepath:
            # restrict to only videos
            self.video_filepath = tkFileDialog.askopenfilename(title="Choose a video file",
                                                               filetypes=[("Video Files", "*.avi *.mp4")])

    @staticmethod
    def is_not_string(string):
        # type: (str) -> bool
        return type(string) is not str

    def print_dictionary(self, output_file):
        for f in self.roi_fish_count:
            for key, value in f.items():
                # is recursive
                if hasattr(value, '__iter__'):
                    self.print_dictionary(value)
                else:
                    output_file.write('{0},'.format(value))
            output_file.write('\n')

    def roi_video(self):
        height, width, ch = self.current_frame.shape
        roi_height = height / n_rows
        roi_width = width / n_columns

        self.roi_mid_width = roi_width
        self.roi_first_height = roi_height
        self.roi_second_height = roi_height * 2

        images = []
        for row in range(0, n_rows):
            for column in range(0, n_columns):
                row_height = row * roi_height
                column_width = column * roi_width
                tmp_image = self.current_frame[
                            row_height: (row + 1) * roi_height,
                            column_width:(column + 1) * roi_width
                            ]
                images.append(tmp_image)

    # todo add possibility to redo the whole frame
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
                cv2.imshow(self.window_name, self.current_frame)
                self.track_fish_through_frames(capture)

    def track_fish_through_frames(self, capture):
        # press n to get to next frame
        if cv2.waitKey(1) % 0xFF == ord('n'):
            #  check if mouse clicked
            if 0 < len(self.current_frame_fish_coord):
                self.frame_no_list.append(capture.get(1))
                self.update_fish_variables()
            else:
                # display the frame number
                cv2.putText(self.current_frame, 'Please first click on a point', (830, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def update_fish_variables(self):
        roi = self.get_no_fish_for_ROI()

        for r in range(len(roi)):
            self.roi_fish_count.append({
                'roi': r + 1,
                'no_fish': roi[r],
                'frame': self.frame_no
            })

    # TODO FIX
    def visualise_coordinates(self):
        self.create_figure(self.all_fish_x_coord, self.all_fish_y_coord, 'X and Y Coordinates', 'y-coordinate (pixel)',
                           'x-coordinate (pixel)')
        # Block=true prevents the graphs from closing immediately
        plt.show(block=True)

    def write_no_fish_to_file(self, filename):
        output_filename = 'Outputs\\fish_no_output_{0}.csv'.format(filename)
        try:
            with open('Outputs\\fish_no_output_{0}.csv'.format(filename), 'w') as output_file:
                self.print_dictionary(output_file)
            output_file.close()
            print("Wrote no fish to file")
        except IOError as e:
            print("Unable to write to a file '{0}'. Writing to a new file '{1}-RETRY'. ({2})"
                  .format(output_filename, filename, e))
            self.write_to_output_file(filename + '-RETRY')

    def write_to_output_file(self, filename):
        """
        Write digitized coordinates into an output file
        :type filename: str
        """
        output_filename = 'Outputs\\output_{0}.csv'.format(filename)
        try:
            with open(output_filename, 'w') as output_file:
                if len(self.all_fish_y_coord) != len(self.all_fish_x_coord):
                    raise Exception('Something went wrong with writing down the coordinates, '
                                    'amount of y and x coordinates is not the same')
                for fish_no in range(len(self.all_fish_x_coord)):
                    output_file.write('{0}, {1} \n'
                                      .format(self.all_fish_x_coord[fish_no], self.all_fish_y_coord[fish_no]))

            output_file.close()
            print("Wrote the outputs")
        except IOError as e:
            print("Unable to write to a file {0}. Writing to a new file. ({1})"
                  .format(output_filename, e))
            self.write_to_output_file(filename + '-RETRY')
