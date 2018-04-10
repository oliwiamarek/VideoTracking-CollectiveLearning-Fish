# coding=utf-8
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position

import cv2
import os
import sys
from FishTracker import FishTracker
from config import MANUAL
from config import calculate_frames, close_capture_window

'''
===========================================================================
FUNCTIONS
===========================================================================
'''


def calculate_video_duration():
    global STOP_FRAME_NO
    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(cap, 1)
    STOP_FRAME_NO = calculate_frames(cap, 2)

    # initialize the starting frame of the video object to start_frame_no
    cap.set(1, start_frame_no)


def print_frame_rate():
    try:
        print('frame rate per second = ' + '%.2f' % cap.get(5))
        print('number of frames = ' + '%.2f' % cap.get(7))
    except TypeError:
        print("Capture.get returned type different to int")
        raise


# TODO move to Fish tracer and make the filepath private
def get_name_from_path():
    try:
        return os.path.splitext(os.path.basename(tracker.video_filepath))[0]
    except TypeError:
        print("Filepath '{0}' incorrect. Cannot extract the file name.".format(tracker.video_filepath))
        raise


def trackFish(capture):
    while capture.isOpened():
        # reset mouse coordinates
        del tracker.current_frame_fish_coord[:]
        if MANUAL:
            tracker.track_fish(capture)
        else:
            tracker.use_background_subtraction(capture)
        if capture.get(1) > STOP_FRAME_NO:
            break


'''
===========================================================================
MAIN FUNCTION
===========================================================================
'''

if __name__ == "__main__":
    try:
        tracker = FishTracker()
        tracker.get_video_file()
        filename = get_name_from_path()

        cap = cv2.VideoCapture(tracker.video_filepath)
        print_frame_rate()
        calculate_video_duration()
        tracker.create_record_window()
        trackFish(cap)

        close_capture_window(cap)
        # TODO have a wrapper around it that calls it with a name that's specified
        tracker.write_to_output_file(filename)
        tracker.write_no_fish_to_file(filename)
        tracker.visualise_coordinates()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
