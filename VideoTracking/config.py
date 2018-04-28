#
# This file contains all of the global variables and the functions that are being used in multiple files in the project.
#


import argparse
import tkFileDialog
from Tkinter import Tk
import numpy
import cv2
import os

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
def construct_argument_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--min-area", type=int, default=MIN_AREA_SIZE, help="minimum area size for contours")
    ap.add_argument("-f", "--waiting-frames", type=int, default=WAITING_FRAMES,
                    help="number of frames used to calculate bcgr model")
    ap.add_argument("-t", "--threshold", type=float, default=THRESHOLD,
                    help="threshold used in bcgr subtraction average calculation")
    return vars(ap.parse_args())


# returns every nth element of the passed array, starting at 'start'
def get_array_increments(array, start, element_no):
    # type: (list, int, int) -> list
    return array[start::element_no]


def is_not_string(string):
    # type: (str) -> bool
    return type(string) is not str


# divide width and height of the video to get boundaries of the ROI
def roi_video(current_frame):
    global roi_first_height, roi_second_height, roi_width

    # get width and height of the video
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


# check if value is between min and max passed in
def is_between(minV, maxV, value):
    # type: (int, int, int) -> bool
    return minV <= value <= maxV


# ask user to select video file. only allow avi and mp4 extensions
def get_video_file():
    # type: () -> str
    title = "Choose a video file"
    types_title = "Video Files"
    types_string = "*.avi *.mp4"
    return get_filepath(title, types_title, types_string)


# ask user for the csv file, used for creation of graphs
def get_csv_file():
    # type: () -> str
    title = "Choose a csv output file"
    types_title = "Output Files"
    types = "*.csv"
    return get_filepath(title, types_title, types)


# ask user for a file, allows only specified file types
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


# this function returns a filename from a filepath passed in as a parameter
def get_name_from_path(path):
    try:
        return os.path.splitext(os.path.basename(path))[0]
    except TypeError:
        print("Filepath '{0}' incorrect. Cannot extract the file name.".format(path))
        raise


# this function was taken from http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
def smooth(x, window_len=11, window='hanning'):
    """smooth the data using a window with requested size.

        This method is based on the convolution of a scaled window with the signal.
        The signal is prepared by introducing reflected copies of the signal
        (with the window size) in both ends so that transient parts are minimized
        in the begining and end part of the output signal.

        input:
            x: the input signal
            window_len: the dimension of the smoothing window; should be an odd integer
            window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
                flat window will produce a moving average smoothing.

        output:
            the smoothed signal

        example:

        t=linspace(-2,2,0.1)
        x=sin(t)+randn(len(t))*0.1
        y=smooth(x)

        see also:

        numpy.hanning, numpy.hamming, numpy.bartlett, numpy.blackman, numpy.convolve
        scipy.signal.lfilter

        TODO: the window parameter could be the window itself if an array instead of a string
        NOTE: length(output) != length(input), to correct this: return y[(window_len/2-1):-(window_len/2)] instead of just y.
        """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len < 3:
        return x

    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    s = numpy.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]
    # print(len(s))
    if window == 'flat':  # moving average
        w = numpy.ones(window_len, 'd')
    else:
        w = eval('numpy.' + window + '(window_len)')

    y = numpy.convolve(w / w.sum(), s, mode='valid')
    return y
