import numpy as np
import cv2

# https://pdfs.semanticscholar.org/8a1f/27fd371eceb8654b735502b810d2094e420b.pdf
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# http://layer0.authentise.com/how-to-track-objects-with-stationary-background.html
# https://medium.com/machine-learning-world/tutorial-making-road-traffic-counting-app-based-on-computer-vision-and-opencv-166937911660

# ===============================================
# import global variables
from FishCoordinates import FishCoordinates
from config import create_window, log, construct_argument_parser, close_capture_window, roi_video, \
    is_between


# ===============================================


class BackgroundSubtractor(object):
    def __init__(self):
        self.args = construct_argument_parser()
        self.background_model = {}
        self.current_frame = {}
        self.fish_coordinates = []
        self.roi_mid_width, self.roi_first_height, self.roi_second_height = 0, 0, 0

    # TODO refactor because it's gross
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
            # raise Exception("Error, fish coordinates list is empty.")
            return []

    def draw_points(self, contours, current_frame):
        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if is_between(self.args["min_area"], 5000, cv2.contourArea(c)):
                # compute the bounding box for the contour, draw it on the frame
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                if self.is_darker_at(cX, cY):
                    coord = FishCoordinates(cX, cY)
                    self.fish_coordinates.append(coord)
                    cv2.circle(current_frame, (cX, cY), 5, (0, 255, 0), -1)
                    if cv2.contourArea(c) > 3000:
                        cv2.drawContours(current_frame, [box], 0, (255, 255, 0), 2)
                        # if bigger than max area, do it twice (means there are at least 2 fish)
                        self.fish_coordinates.append(coord)
                    else:
                        cv2.drawContours(current_frame, [box], 0, (0, 0, 255), 2)

    # convert current frame to grey scale and blur it
    def convert_to_grey_scale_and_blur(self, current_frame):
        difference_image = cv2.absdiff(self.background_model, current_frame)
        create_window("Frame Difference", difference_image)
        gray = cv2.cvtColor(difference_image, cv2.COLOR_BGR2GRAY) if len(
            difference_image.shape) == 3 else difference_image
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        log("Successfully converted to greyscale and blurred.")
        return gray

    # dilate the threshold image to fill in holes, then find contours on threshold image
    def find_contours(self, thresh):
        im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        log("Successfully found contours.")
        contours = [cv2.approxPolyDP(contour, 0.01, True) for contour in contours]
        return contours

    def use_background_subtraction_on(self, current_frame):
        gray = self.convert_to_grey_scale_and_blur(current_frame)

        # compute the absolute difference between the current frame and background frame
        threshold = cv2.dilate(cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
        contours = self.find_contours(threshold)

        self.draw_points(contours, current_frame)

        log("Coord(x then y):")
        log([coord.x for coord in self.fish_coordinates])
        log([coord.y for coord in self.fish_coordinates])

        create_window("Frame", current_frame)
        create_window("Foreground", threshold)

    def is_darker_at(self, xCoord, yCoord):
        # type: (int, int) -> bool
        # if coordinates between x miedzy 1 a 239 and y miedzy 3 a 444 - sprawdz czy kolor ciemnoszary > 50
        frame_brightness = self.get_brightness_of(self.current_frame, xCoord, yCoord)
        background_brightness = self.get_brightness_of(self.background_model, xCoord, yCoord)
        if is_between(183, 369, xCoord) and is_between(0, 270, yCoord):
            return False
        elif is_between(150, 1200, xCoord) and is_between(100, 650, yCoord):
            return (background_brightness - frame_brightness) > -10
        else:
            return (background_brightness - frame_brightness) > -10

    def get_brightness_of(self, frame, xCoord, yCoord):
        # type: (object, int, int) -> int
        R, G, B = frame[yCoord, xCoord]
        return (R + G + B) / 3


# =====================================================================================================================

if __name__ == "__main__":
    bcgr = BackgroundSubtractor()
    video_source = "ExampleVid/trial2.mp4"
    bcgr.create_background_model(video_source)
    # start video file/webcam stream
    cam = cv2.VideoCapture(video_source)

    while 1:
        bcgr.detect_fish(cam)

        # if the `q` key is pressed, break from the lop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            log("Pressed 'q' to exit.")
            break
    close_capture_window(cam)
    log("Process finished.")
