# coding=utf-8
# Otar Akanyeti
# 16 July 2017
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position manually

import cv2
import os
import sys
import FishTracker

'''
GLOBAL FUNCTIONS 
'''
stop_frame_no = 0


def calculate_frames(capture, seconds):
    try:
        return int(seconds * capture.get(5))
    except TypeError:
        print("Cannot calculate frames due to wrong values: seconds: {0}, capture: {1}".format(seconds, capture.get(5)))
        raise


def calculate_video_duration():
    global stop_frame_no
    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(cap, 1)
    stop_frame_no = calculate_frames(cap, 2)

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


'''
MAIN FUNCTION
'''

if __name__ == "__main__":
    try:
        tracker = FishTracker.FishTracker()

        tracker.get_video_file()
        filename = get_name_from_path()

        cap = cv2.VideoCapture(tracker.video_filepath)

        print_frame_rate()

        calculate_video_duration()
        tracker.create_record_window()

        while cap.isOpened():
            tracker.track_fish(cap)
            if cap.get(1) > stop_frame_no:
                break

        tracker.close_capture_window(cap)

        tracker.write_to_output_file(filename)
        tracker.visualise_coordinates()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
