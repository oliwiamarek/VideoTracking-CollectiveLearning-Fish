#
# This file contains all of the global variables and the functions that are being used in multiple files in the project.
#


import argparse
import tkFileDialog
from Tkinter import Tk

import cv2


'''
===========================================================================
GLOBAL VARIABLES
===========================================================================
'''

MANUAL = False  # Flag to use the manual or automated version of code
DEBUG = True  # used to print debug logs
WAITING_FRAMES = 900  # default number of frames used to calculate bcgr model
MIN_AREA_SIZE = 500  # default minimum area size for contours
THRESHOLD = 0.01  # default value of threshold used in bcgr subtraction average calculation
N_ROI_ROWS = 2
N_ROI_COLUMNS = 3

'''
===========================================================================
GLOBAL FUNCTIONS
===========================================================================
'''


# Used for printing out things for debugging purposes
def log(s):
    # type: (str) -> type(None)
    if DEBUG:
        print s


def create_window(title, variable):
    # type: (str, object) -> None
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, variable)


def close_capture_window(capture):
    capture.release()
    cv2.destroyAllWindows()


# construct the argument parser and parse the arguments
# look https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
def construct_argument_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--min-area", type=int, default=MIN_AREA_SIZE, help="minimum area size for contours")
    ap.add_argument("-f", "--waiting-frames", type=int, default=WAITING_FRAMES,
                    help="number of frames used to calculate bcgr model")
    ap.add_argument("-t", "--threshold", type=float, default=THRESHOLD,
                    help="threshold used in bcgr subtraction average calculation")
    return vars(ap.parse_args())


def get_array_increments(array, start, element_no):
    # type: (list, int, int) -> list
    return array[start::element_no]


def is_not_string(string):
    # type: (str) -> bool
    return type(string) is not str


def roi_video(current_frame):
    global roi_first_height, roi_second_height, roi_width
    width, height, ch = current_frame.shape
    roi_width = width / N_ROI_ROWS + 20
    roi_first_height = height / N_ROI_COLUMNS
    roi_second_height = roi_first_height * 2


def roi_first_height():
    return roi_first_height


def roi_second_height():
    return roi_second_height


def roi_width():
    return roi_width


def is_between(minV, maxV, value):
    # type: (int, int, int) -> bool
    return minV <= value <= maxV


def get_video_file():
    # type: () -> str
    title = "Choose a video file"
    types_title = "Video Files"
    types_string = "*.avi *.mp4"
    return get_filepath(title, types_title, types_string)


def get_csv_file():
    # type: () -> str
    title = "Choose a csv output file"
    types_title = "Output Files"
    types = "*.csv"
    return get_filepath(title, types_title, types)


def get_filepath(title, file_types_title, file_types_str):
    # type: (str, str, str) -> str
    # hides the Tk window
    video_filepath = {}
    root = Tk()
    root.withdraw()
    # ask for video file
    while not video_filepath:
        # restrict to only videos
        video_filepath = tkFileDialog.askopenfilename(title=title, filetypes=[(file_types_title, file_types_str)])
    return video_filepath
