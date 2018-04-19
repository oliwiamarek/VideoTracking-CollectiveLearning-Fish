import cv2
import matplotlib.pyplot as plt
from BackgroundSubtractor import BackgroundSubtractor as BackgroundSubtraction
from config import get_array_increments, is_not_string, log, roi_video, roi_width, roi_second_height, roi_first_height

"""
FISH TRACKER CLASS
https://introlab.github.io/find-object/s
http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher
"""


class FishTracker(object):
    def __init__(self):
        self.current_frame_fish_coord, self.all_fish_x_coord, self.all_fish_y_coord = [], [], []
        self.roi_fish_count, self.frame_no_list = [], []
        self.current_frame, self.previous_frame = {}, {}
        self.window_name = "Fishies"
        self.frame_no = 0
        self.bcg_subtraction = BackgroundSubtraction()

    def create_background_model(self):
        self.bcg_subtraction.create_background_model()
        log("Start Fish detection.")

    # no test
    def create_figure(self, x_axis, y_axis, title, x_label, y_label):
        """
        :type x_axis: List[int]
        :type y_axis: List[int]
        :type title: str
        :type x_label: str
        :type y_label: str
        """
        if is_not_string(title) or is_not_string(x_label) or is_not_string(y_label):
            raise TypeError("Title or labels not strings. Wrong type.")
        plt.figure()
        no_fish = len(self.current_frame_fish_coord)
        for x in xrange(no_fish):
            plt.plot(get_array_increments(x_axis, x, no_fish + 1), get_array_increments(y_axis, x, no_fish + 1))
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

    # no test
    def create_record_window(self):
        self.window_name = 'Fishies'
        # normalize size of the window to every screen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    # no test
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
            self.current_frame_fish_coord.append('{0}, {1}'.format(y, x))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.current_frame = self.previous_frame.copy()
            del self.current_frame_fish_coord[-1]

    # todo test
    def get_no_fish_for_ROI(self):
        roi = [0, 0, 0, 0, 0, 0]
        for fish in self.current_frame_fish_coord:
            coordinates = [int(x.strip()) for x in fish.split(',')]
            x = coordinates[0]
            y = coordinates[1]
            self.all_fish_x_coord.append(x)
            self.all_fish_y_coord.append(y)
            if x < roi_width() and y < roi_first_height():
                roi[0] += 1
            elif x < roi_width() and y < roi_second_height():
                roi[1] += 1
            elif x < roi_width() and y > roi_second_height():
                roi[2] += 1
            elif x > roi_width() and y < roi_first_height():
                roi[3] += 1
            elif x > roi_width() and y < roi_second_height():
                roi[4] += 1
            elif x > roi_width() and y > roi_second_height():
                roi[5] += 1
        self.all_fish_x_coord.append("")
        self.all_fish_y_coord.append("")
        return roi

    def print_dictionary(self, output_file):
        for f in self.roi_fish_count:
            for key, value in f.items():
                # is recursive
                if hasattr(value, '__iter__'):
                    self.print_dictionary(value)
                else:
                    output_file.write('{0},'.format(value))
            output_file.write('\n')

    # todo add possibility to redo the whole frame
    def track_fish(self, capture):
        # read next frame
        ret, frame = capture.read()
        self.current_frame = frame
        self.previous_frame = self.current_frame.copy()
        # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # possibly move to outside the loop
        roi_video()

        if ret:  # check if the frame has been read properly
            fr_len = len(self.frame_no_list)

            self.display_frame_text(self.current_frame, capture)
            # clicking at fish adds a circular point - has to be outside the while loop
            cv2.setMouseCallback(self.window_name, self.draw_point)

            while fr_len == len(self.frame_no_list):
                cv2.imshow(self.window_name, self.current_frame)
                self.track_fish_through_frames(capture)

    # no test
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

    def use_background_subtraction(self, cap):
        current_fish_coord = self.bcg_subtraction.detect_fish(cap)
        if current_fish_coord:
            self.current_frame_fish_coord = current_fish_coord
            self.frame_no_list.append(cap.get(1))
            self.update_fish_variables()

    def visualise_coordinates(self):
        self.create_figure(self.all_fish_x_coord, self.all_fish_y_coord, 'X and Y Coordinates', 'y-coordinate (pixel)',
                           'x-coordinate (pixel)')
        # Block=true prevents the graphs from closing immediately
        plt.show(block=True)

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
