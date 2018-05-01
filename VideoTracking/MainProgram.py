# Oliwia Marek (okm@aber.ac.uk)
# 25 April 2018
# This program enables the user to digitize fish position and count the number of fish in different regions of interest.
# Depending on the flag MANUAL set in the config file, user will be able to perform a manual or automated detection and
# counting of the fish. There is also DEBUG flag in config file that allows outputting more information during runtime
# for debugging purposes.
# User first is prompt to select the video file and then has to either: wait for the background subtraction to
# automatically perform the task, or click on all of the fish in the frame and press 'n' to go to the next frame.
# Program outputs two files: one containing all fish coordinates and one containing the number of fish in each region
# All code was written by me unless clearly specified.
#
# This file contains the main function of the program.

import cv2
import sys

from FishTracker import FishTracker
from config import MANUAL, close_capture_window, log, get_video_file, get_name_from_path

'''
===========================================================================
FUNCTIONS
===========================================================================
'''


def calculate_video_duration(capture):
    global stop_frame_no
    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(capture, 1)
    stop_frame_no = calculate_frames(capture, capture.get(7) / capture.get(5))
    # initialize the starting frame of the video object to start_frame_no
    capture.set(1, start_frame_no)


# frame rate printing in the terminal
def print_frame_rate(capture):
    try:
        log("frame rate per second = " + "%.2f" % capture.get(5))
        log("number of frames = " + "%.2f" % capture.get(7))
    except TypeError:
        print("Capture.get returned type different to float")
        raise


# this function performs background subtraction or manual tracking depending on flags specified in config
def track_fish(capture):
    print("Starting Fish detection.")
    # is manual flag set to true, create record window for manual tracking
    if MANUAL:
        tracker.create_record_window()
    else:
        tracker.create_background_model(filePath)
    while capture.isOpened():
        if capture.get(1) >= stop_frame_no:
            log("Frame number ({0}) bigger than stop frame no ({1})".format(capture.get(1), stop_frame_no))
            break

        # reset mouse coordinates
        del tracker.current_frame_fish_coord[:]

        if MANUAL:  # if manual flag set to false, perform manual tracking
            tracker.track_fish(capture)
        else:  # if manual flag set to false, perform background subtraction
            tracker.use_background_subtraction(capture)
        # if the `q` key is pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            log("Pressed 'q' to exit.")
            break


# calculate number of frames in duration passed in.
def calculate_frames(capture, seconds):
    try:
        return int(seconds * capture.get(5))
    except TypeError:
        print("Cannot calculate frames due to wrong values: seconds: {0}, capture: {1}".format(seconds, capture.get(5)))
        raise


'''
===========================================================================
MAIN FUNCTION
===========================================================================
'''

if __name__ == "__main__":
    try:
        tracker = FishTracker()  # create fish tracker class object
        filePath = get_video_file()  # asks user to select a video file
        filename = get_name_from_path(filePath)  # get name from filepath
        cap = cv2.VideoCapture(filePath)

        print_frame_rate(cap)
        calculate_video_duration(cap)
        track_fish(cap)
        close_capture_window(cap)  # finish tracking
        log("Tracking process finished.")

        # Write output to files
        tracker.write_to_output_file(filename)
        tracker.write_no_fish_to_file(filename)
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
