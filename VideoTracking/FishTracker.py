#
# This file contains the Fish Tracker class. This class is used for manual tracking and counting of the fish.
# It also has functions for writing to the output files.

import cv2
from BackgroundSubtractor import BackgroundSubtractor as BackgroundSubtraction
from FishCoordinates import FishCoordinates
from config import log, roi_video, roi_width, roi_second_height, roi_first_height

"""
===========================================================================
FISH TRACKER CLASS
===========================================================================
"""


class FishTracker(object):
    def __init__(self):
        self.current_frame_fish_coord, self.all_fish_coord = [], []  # current and overall list of fish coordinates
        self.roi_fish_count = []  # count of fish in each of the ROI in every frame
        self.frame_no_list = []  # list of the frame numbers to be used in the output file creation
        self.current_frame, self.previous_frame = {}, {}  # variables to store current and previous frame
        self.window_name = "Fishies"  # name of the main window for Manual Tracking
        self.frame_no = 0  # current frame number
        self.bcg_subtractor = BackgroundSubtraction()  # Background Subtractor object

    def create_background_model(self, path):
        self.bcg_subtractor.create_background_model(path)
        log("Start Fish detection.")

    def create_record_window(self):
        self.window_name = 'Fishies'
        # normalize size of the window to every screen
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)

    def display_frame_text(self, frame, capture):
        self.frame_no = capture.get(1)
        cv2.putText(frame, 'frame ' + str(self.frame_no), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), 2)
        cv2.putText(self.current_frame, 'Right click to undo', (830, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # function to draw the point after clicking on the fish manually. User can right click to undo once.
    def draw_point(self, event, x, y, flags, params):
        # if left click, draw point
        if event == cv2.EVENT_LBUTTONDOWN:
            self.previous_frame = self.current_frame.copy()
            cv2.circle(self.current_frame, (x, y), 5, (0, 255, 0), -1)
            coord = FishCoordinates(x, y)
            self.current_frame_fish_coord.append(coord)
        # if right click, undo the previous click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.current_frame = self.previous_frame.copy()
            del self.current_frame_fish_coord[-1]

    # this function loops through coordinates of current frame and counts in which ROI the fish is situated
    def get_no_fish_for_ROI(self):
        # type: () -> [int]
        roi = [0, 0, 0, 0, 0, 0]
        for fish in self.current_frame_fish_coord:
            x = fish.getX()
            y = fish.getY()

            # update list with all coordinates
            self.all_fish_coord.append(fish)

            # 1st ROI in upper left corner, 6th ROI in bottom right corner
            if y < roi_width() and x < roi_first_height():
                roi[0] += 1
            elif y < roi_width() and x < roi_second_height():
                roi[1] += 1
            elif y < roi_width() and x > roi_second_height():
                roi[2] += 1
            elif y > roi_width() and x < roi_first_height():
                roi[3] += 1
            elif y > roi_width() and x < roi_second_height():
                roi[4] += 1
            elif y > roi_width() and x > roi_second_height():
                roi[5] += 1

        # add empty row after each frame
        self.all_fish_coord.append("")
        return roi

    # this function is printing the dictionary recursively into a file passed in.
    def print_dictionary(self, output_file):
        for f in self.roi_fish_count:
            for key, value in f.items():
                # check if recursive
                if hasattr(value, '__iter__'):
                    self.print_dictionary(value)
                else:
                    output_file.write('{0},'.format(value))
            output_file.write('\n')

    def track_fish(self, capture):
        # read next frame
        ret, frame = capture.read()
        self.current_frame = frame
        self.previous_frame = self.current_frame.copy()

        roi_video(frame)

        # only continue if the frame has been read properly
        if ret:
            fr_len = len(self.frame_no_list)
            self.display_frame_text(self.current_frame, capture)

            # clicking at fish adds a circular point
            cv2.setMouseCallback(self.window_name, self.draw_point)

            while fr_len == len(self.frame_no_list):
                cv2.imshow(self.window_name, self.current_frame)
                self.track_fish_through_frames(capture)

    # function to update fish lists once key 'n' is pressed to go to the next frame
    def track_fish_through_frames(self, capture):
        # press n to get to next frame
        if cv2.waitKey(1) % 0xFF == ord('n'):
            #  check if mouse clicked
            if 0 < len(self.current_frame_fish_coord):
                self.frame_no_list.append(capture.get(1))
                self.update_roi_fish_count()
            # if mouse not clicked, do not continue
            else:
                cv2.putText(self.current_frame, 'Please first click on a point', (830, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def update_roi_fish_count(self):
        roi = self.get_no_fish_for_ROI()

        for r in range(len(roi)):
            self.roi_fish_count.append({
                'roi': r + 1,
                'no_fish': roi[r]
            })

    # use background subtraction instead of manual tracking and update variables
    def use_background_subtraction(self, cap):
        self.frame_no = cap.get(1)
        current_fish_coord = self.bcg_subtractor.detect_fish(cap)
        if current_fish_coord:
            self.current_frame_fish_coord = current_fish_coord
            self.frame_no_list.append(cap.get(1))
            self.update_roi_fish_count()

    # write fish coordinates into a file with the same name is video
    def write_to_output_file(self, filename):
        output_filename = 'Outputs\\output_{0}.csv'.format(filename)
        try:
            with open(output_filename, 'w') as output_file:
                # check if more than one frame was read
                if len(self.all_fish_coord) == len(self.current_frame_fish_coord):
                    raise Exception('Something went wrong with writing down the coordinates, '
                                    'only wrote down coordinates from one frame')
                # loop through all coordinates and output into a file
                for fish_no in range(len(self.all_fish_coord)):
                    coord = self.all_fish_coord[fish_no]
                    if type(coord) is str:  # if it is a fish coordinates separator (empty string), print it
                        output_file.write('{0} \n'.format(coord))
                    else:
                        output_file.write('{0}, {1} \n'.format(coord.getX(), coord.getY()))
            output_file.close()
            print("Wrote the outputs")
        except IOError as e:
            print("Unable to write to a file {0}. Writing to a new file. ({1})".format(output_filename, e))
            # if file was readonly or unable to write to, retry with added string at the end of the filename
            self.write_to_output_file(filename + '-RETRY')

    # write the information about ROI into a file
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
            # if file was readonly or unable to write to, retry with added string at the end of the filename
            self.write_to_output_file(filename + '-RETRY')
