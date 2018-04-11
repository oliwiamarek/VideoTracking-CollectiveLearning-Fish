# coding=utf-8
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position

import tkFileDialog
from Tkinter import Tk

import cv2
import os
import sys

from FishTracker import FishTracker
from config import MANUAL, close_capture_window, log

'''
===========================================================================
FUNCTIONS
===========================================================================
'''


def get_video_file():
    # hides the Tk window
    video_filepath = {}
    root = Tk()
    root.withdraw()
    # ask for video file
    while not video_filepath:
        # restrict to only videos
        video_filepath = tkFileDialog.askopenfilename(title="Choose a video file",
                                                      filetypes=[("Video Files", "*.avi *.mp4")])
    return video_filepath


def calculate_video_duration():
    global stop_frame_no
    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(cap, 1)
    stop_frame_no = calculate_frames(cap, 40)

    # initialize the starting frame of the video object to start_frame_no
    cap.set(1, start_frame_no)


def print_frame_rate():
    try:
        print('frame rate per second = ' + '%.2f' % cap.get(5))
        print('number of frames = ' + '%.2f' % cap.get(7))
    except TypeError:
        print("Capture.get returned type different to int")
        raise


def get_name_from_path(path):
    try:
        return os.path.splitext(os.path.basename(path))[0]
    except TypeError:
        print("Filepath '{0}' incorrect. Cannot extract the file name.".format(path))
        raise


def track_fish(capture):
    times = 0
    print("Start Fish detection.")
    if MANUAL:
        tracker.create_record_window()
    else:
        tracker.create_background_model()
    while capture.isOpened():
        times += 1
        log("TIMES: {0}".format(times))
        # reset mouse coordinates
        del tracker.current_frame_fish_coord[:]
        if MANUAL:
            tracker.track_fish(capture)
        else:
            tracker.use_background_subtraction(capture)
        if capture.get(1) > stop_frame_no:
            log("Frame number ({0}) bigger than stop frame no ({1})".format(capture.get(1), stop_frame_no))
            break
        # if the `q` key is pressed, break from the loop
        # Turns out I needed to let OpenCV start handling events. The cv::waitKey(n) function in OpenCV is used to
        # introduce a delay of n milliseconds while rendering images to windows
        # https://codeyarns.com/2015/01/20/how-to-use-opencv-waitkey-in-python/
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            log("Pressed 'q' to exit.")
            break


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
        tracker = FishTracker()
        filePath = get_video_file()
        filename = get_name_from_path(filePath)
        cap = cv2.VideoCapture(filePath)

        print_frame_rate()
        calculate_video_duration()
        track_fish(cap)
        close_capture_window(cap)
        log("Tracking process finished.")

        tracker.write_to_output_file(filename)
        tracker.write_no_fish_to_file(filename)
        tracker.visualise_coordinates()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
