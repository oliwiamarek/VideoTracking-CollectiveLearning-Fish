#
# This file contains a Background Subtractor class that performs automated detection and counting of the fish.
# It first creates a background model and then subtracts the current frame from it to detect the movement.
# It also consists of filtering function to get rid of the noise.
#

import numpy as np
import cv2

from FishCoordinates import FishCoordinates
from config import create_window, log, construct_argument_parser, roi_video, is_between


"""
===========================================================================
BACKGROUND SUBTRACTOR CLASS
===========================================================================
"""


class BackgroundSubtractor(object):
    def __init__(self):
        # get argument parser to read values needed for background model creation
        self.args = construct_argument_parser()
        self.background_model = {}
        self.current_frame = {}
        self.fish_coordinates = []  # lists of fish coordinates of current frame
        self.roi_mid_width, self.roi_first_height, self.roi_second_height = 0, 0, 0  # boundaries of ROI

    # This function takes a filename as a string and calculates and outputs a background model
    def create_background_model(self, video_filename):
        no_waiting_frames = self.args["waiting_frames"]
        bcgr_model = {}
        # start video file/webcam stream
        camera = cv2.VideoCapture(video_filename)
        print("Calculating the background model. Please wait {0} seconds".format(no_waiting_frames / camera.get(5)))
        ret, frame = camera.read()
        moving_average = np.float32(frame)
        for i in range(no_waiting_frames):
            grabbed, current_frame = camera.read()
            # if frame could not be grabbed, we reached the end of video
            if not grabbed:
                break
            cv2.accumulateWeighted(current_frame, moving_average, self.args["threshold"])
            # do the drawing stuff
            bcgr_model = cv2.convertScaleAbs(moving_average)
            log("Frame number: {0} done successfully.".format(i))
        print("Model calculated")
        if bcgr_model is None:
            log("bcgrModel not assigned.")
            raise NameError("BcgrModel not assigned")
        camera.release()
        log("Opened background model window for: {0}".format(bcgr_model))
        self.background_model = bcgr_model
        cv2.imwrite("Outputs/backgroundModel.png", bcgr_model)
        # show the background model
        create_window("Background Model", self.background_model)

    # this function performs background subtraction on a current frame. It takes a video capture object from OpenCV
    def detect_fish(self, camera):
        grabbed, current_frame = camera.read()
        self.current_frame = current_frame

        # if frame could not be grabbed, we reached the end of video
        if grabbed:
            roi_video(current_frame)
            self.use_background_subtraction_on(current_frame)
            if self.fish_coordinates:
                return self.fish_coordinates
            # if no fish found, raise an exception
            raise Exception("Error, fish coordinates list is empty.")

    # function to create contours and points on detected fish. Takes array of detected contours and
    # an object of current frame
    def draw_points(self, contours, current_frame):
        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if is_between(self.args["min_area"], 5000, cv2.contourArea(c)):
                # compute the bounding box for the contour, draw it on the frame
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # use moments to acquire x and y coordinates
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # if detected is darker than background, assume it is a fish
                if self.is_a_bubble(cX, cY):
                    coord = FishCoordinates(cX, cY)
                    self.fish_coordinates.append(coord)
                    # draw a point
                    cv2.circle(current_frame, (cX, cY), 5, (0, 255, 0), -1)

                    # if bigger than max area, do it twice (means there are at least 2 fish)
                    if cv2.contourArea(c) > 3000:
                        cv2.drawContours(current_frame, [box], 0, (255, 255, 0), 2)
                        self.fish_coordinates.append(coord)
                    else:
                        cv2.drawContours(current_frame, [box], 0, (0, 0, 255), 2)

    # convert current frame to grey scale and blur it. It takes an object of current frame and returns edited frame
    def convert_to_grey_scale_and_blur(self, current_frame):
        # calculate absolute difference between model and current frame and display it
        difference_image = cv2.absdiff(self.background_model, current_frame)
        create_window("Frame Difference", difference_image)
        # convert to grey scale
        gray = cv2.cvtColor(difference_image, cv2.COLOR_BGR2GRAY) if len(
            difference_image.shape) == 3 else difference_image
        # blur the image
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        log("Successfully converted to greyscale and blurred.")
        return gray

    # dilate the threshold image to fill in holes, then find contours on image and return them as a list
    def find_contours(self, thresh):
        im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        log("Successfully found contours.")
        contours = [cv2.approxPolyDP(contour, 0.01, True) for contour in contours]
        return contours

    # perform background subtraction on current frame and display final effect
    def use_background_subtraction_on(self, current_frame):
        gray = self.convert_to_grey_scale_and_blur(current_frame)

        # compute the absolute difference between the current frame and background frame
        threshold = cv2.dilate(cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
        contours = self.find_contours(threshold)

        # draw points and contours on all detected fish
        self.draw_points(contours, current_frame)

        log("Coord(x then y):")
        log([coord.x for coord in self.fish_coordinates])
        log([coord.y for coord in self.fish_coordinates])

        # display current frame and the foreground calculated
        create_window("Frame", current_frame)
        create_window("Foreground", threshold)

    # check if detected movement is a fish (darker than the background). It takes 2 integers as detected coordinates
    def is_a_bubble(self, xCoord, yCoord):
        # type: (int, int) -> bool
        # if coordinates between x miedzy 1 a 239 and y miedzy 3 a 444 - sprawdz czy kolor ciemnoszary > 50
        frame_brightness = self.get_brightness_of(self.current_frame, xCoord, yCoord)
        background_brightness = self.get_brightness_of(self.background_model, xCoord, yCoord)
        # if in the dark areas of the video, assume it is a fish
        if is_between(183, 369, xCoord) and is_between(0, 270, yCoord):
            return False
        # if in the main area or bubble area, check if detected is darker than the background
        elif is_between(150, 1200, xCoord) and is_between(100, 650, yCoord):
            return (background_brightness - frame_brightness) > -10
        else:
            return (background_brightness - frame_brightness) > -10

    # get brightness by averaging the values of red, green and blue of the pixel
    def get_brightness_of(self, frame, xCoord, yCoord):
        R, G, B = frame[yCoord, xCoord]
        return (R + G + B) / 3
