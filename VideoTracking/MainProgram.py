# coding=utf-8
# Otar Akanyeti
# 16 July 2017
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position manually

import matplotlib.pyplot as plt
import cv2
import os
import sys

import FishTracker

'''
GLOBAL FUNCTIONS 
'''
mX, mY = -1, -1
frame = 0
save_exp_var = False


def calculate_frames(capture, seconds):
    return int(seconds * capture.get(5))


def exit_program(capture):
    capture.release()
    cv2.destroyAllWindows()


def draw_circle(event, x, y, flags, params):
    global mX, mY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        mX, mY = x, y


'''
MAIN FUNCTION
'''

if __name__ == "__main__":
    try:
        tracker = FishTracker.FishTracker()

        tracker.get_video_file()
        # get name from path
        filename = os.path.splitext(os.path.basename(tracker.video_filepath))[0]

        cap = cv2.VideoCapture(tracker.video_filepath)

        print('frame rate per second = ' + '%.2f' % cap.get(5))
        print('number of frames = ' + '%.2f' % cap.get(7))

        # calculate start and stop frames (normalized between 0 and 1)
        start_frame_no = calculate_frames(cap, 1)
        stop_frame_no = calculate_frames(cap, 2)

        # initialize the starting frame of the video object to start_frame_no
        cap.set(1, start_frame_no)

        # create a window
        window_name = 'Fishies'
        # normalize size of the window to every screen
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        while cap.isOpened():

            # read next frame
            ret, frame = cap.read()

            if ret:  # check if the frame has been read properly
                fr_len = len(tracker.fr)

                # display the frame number
                cv2.putText(frame, 'frame ' + str(cap.get(1)), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)
                # clicking at fish adds a circular point - has to be outside the while loop
                cv2.setMouseCallback(window_name, draw_circle)

                '''https://www.learnopencv.com/read-write-and-display-a-video-using-opencv-cpp-python/ After reading 
                a video file, we can display the video frame by frame. A frame of a video is simply an image and we 
                display each frame the same way we display images, i.e., we use the function imshow(). '''
                '''As in the case of an image, we use the waitKey() after imshow() function to pause each frame in 
                the video. In the case of an image, we pass ‘0’ to the waitKey() function, but for playing a video, 
                we need to pass a number greater than ‘0’ to the waitKey() function. This is because ‘0’ would pause 
                the frame in the video for an infinite amount of time and in a video we need each frame to be shown 
                only for some finite interval of time, so we need to pass a number greater than ‘0’ to the waitKey() 
                function. This number is equal to the time in milliseconds we want each frame to be displayed. '''
                '''While reading the frames from a webcam, using waitKey(1) is appropriate because the display frame 
                rate will be limited by the frame rate of the webcam even if we specify a delay of 1 ms in waitKey. 
                While reading frames from a video that you are processing, it may still be appropriate to set the 
                time delay to 1 ms so that the thread is freed up to do the processing we want to do. '''
                while fr_len == len(tracker.fr):
                    cv2.imshow(window_name, frame)  # show it
                    if cv2.waitKey(1) % 0xFF == ord('n'):
                        if mX > -1 and mY > -1:
                            tracker.fr.append(cap.get(1))
                            tracker.fishX.append(mX)
                            tracker.fishY.append(mY)
                            mX, mY = -1, -1
                        else:
                            cv2.putText(frame, 'Please first click on a point', (830, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                        (0, 0, 255), 2)  # display the frame number

                if save_exp_var:
                    save_exp_var = False
                    # select_dipole_and_food()

                    # write_to_variable_file()

            if cap.get(1) > stop_frame_no:
                break

        exit_program(cap)

        # write digitized coordinates into an output file
        tracker.write_to_output_file(filename)

        tracker.visualise_coordinates()
    except:
        print ("Unexpected error:", sys.exc_info()[0])
        raise
