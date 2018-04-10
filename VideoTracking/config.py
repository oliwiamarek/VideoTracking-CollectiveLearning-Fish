import cv2

'''
===========================================================================
GLOBAL VARIABLES
===========================================================================
'''

STOP_FRAME_NO = 0
MANUAL = True
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


def createWindow(title, variable):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, variable)


def calculate_frames(capture, seconds):
    try:
        return int(seconds * capture.get(5))
    except TypeError:
        print("Cannot calculate frames due to wrong values: seconds: {0}, capture: {1}".format(seconds, capture.get(5)))
        raise


def close_capture_window(capture):
    capture.release()
    cv2.destroyAllWindows()
