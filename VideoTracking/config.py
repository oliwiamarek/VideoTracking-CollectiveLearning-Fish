import argparse
import cv2

'''
===========================================================================
GLOBAL VARIABLES
===========================================================================
'''

MANUAL = True  # Flag to use the manual or automated version of code
VIDEO_SOURCE = "ExampleVid/week4.mp4"  # path to video
DEBUG = True  # used to print debug logs
WAITING_FRAMES = 200  # default number of frames used to calculate bcgr model
MIN_AREA_SIZE = 1300  # default minimum area size for contours
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
    if DEBUG:
        print s


def create_window(title, variable):
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


def return_array(array, start, element_no):
    return array[start::element_no]


def is_not_string(string):
    # type: (str) -> bool
    return type(string) is not str