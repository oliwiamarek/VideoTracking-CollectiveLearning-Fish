import numpy as np
import cv2

# https://pdfs.semanticscholar.org/8a1f/27fd371eceb8654b735502b810d2094e420b.pdf
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# http://layer0.authentise.com/how-to-track-objects-with-stationary-background.html
# https://medium.com/machine-learning-world/tutorial-making-road-traffic-counting-app-based-on-computer-vision-and-opencv-166937911660

# ===============================================
# import global variables
from config import VIDEO_SOURCE, create_window, log, construct_argument_parser, close_capture_window, N_ROI_ROWS, \
    N_ROI_COLUMNS

X_COORD = []
Y_COORD = []


# ===============================================


class BackgroundSubtractionModel(object):
    def __init__(self):
        self.args = construct_argument_parser()
        self.backgroundModel = {}
        self.current_frame = {}
        self.roi_mid_width, self.roi_first_height, self.roi_second_height = 0, 0, 0

    # TODO refactor because it's gross
    def create_background_model(self):
        noWaitingFrames = self.args["waiting_frames"]
        bcgrModel = {}
        # start video file/webcam stream
        camera = cv2.VideoCapture(VIDEO_SOURCE)
        print("Calculating the background model. Please wait {0} seconds".format(noWaitingFrames / camera.get(5)))
        ret, frame = camera.read()
        movingAverage = np.float32(frame)
        for i in range(noWaitingFrames):
            grabbed, current_frame = camera.read()
            # if frame could not be grabbed, we reached the end of video
            if not grabbed:
                break
            cv2.accumulateWeighted(current_frame, movingAverage, self.args["threshold"])
            # do the drawing stuff
            bcgrModel = cv2.convertScaleAbs(movingAverage)
            log("Frame number: {0} done successfully.".format(i))
        print("Model calculated")
        if bcgrModel is None:
            log("bcgrModel not assigned.")
            raise NameError("BcgrModel not assigned")
        camera.release()
        log("Opened background model window for: {0}".format(bcgrModel))
        self.backgroundModel = bcgrModel
        # show the background model
        create_window("Background Model", self.backgroundModel)

    def detect_fish(self, camera):
        grabbed, currentFrame = camera.read()
        self.current_frame = currentFrame
        self.roi_video()

        # if frame could not be grabbed, we reached the end of video
        if grabbed:
            self.use_background_subtraction_on(currentFrame)

    def draw_points(self, contours, currentFrame):
        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < self.args["min_area"]:
                continue
            # compute the bounding box for the contour, draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            X_COORD.append(x)
            Y_COORD.append(y)
            # x + w/2 because (x,y) is top left corner of contour, (x+w, y+h) is bottom right so the halves are middle
            cv2.circle(currentFrame, (x + w / 2, y + h / 2), 5, (0, 255, 0), -1)

    # convert current frame to grey scale and blur it
    def convert_to_grey_scale_and_blur(self, currentFrame):
        differenceImage = cv2.absdiff(self.backgroundModel, currentFrame)
        create_window("Frame Delta", differenceImage)
        gray = cv2.cvtColor(differenceImage, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        log("Successfully converted to greyscale and blurred.")
        return gray

    # dilate the threshold image to fill in holes, then find contours on threshold image
    def find_contours(self, thresh):
        im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        log("Successfully found contours.")
        return contours

    def use_background_subtraction_on(self, currentFrame):
        gray = self.convert_to_grey_scale_and_blur(currentFrame)

        # compute the absolute difference between the current frame and background frame
        threshold = cv2.dilate(cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
        contours = self.find_contours(threshold)

        self.draw_points(contours, currentFrame)

        # self.frame_no_list.append(capture.get(1))
        # self.update_fish_variables()

        log("X coord: {0}".format(X_COORD))
        log("Y coord: {0}".format(Y_COORD))
        del X_COORD[:]
        del Y_COORD[:]

        create_window("Frame", currentFrame)
        create_window("Foreground", threshold)

    def roi_video(self):
        height, width, ch = self.current_frame.shape
        roi_height = height / N_ROI_ROWS
        roi_width = width / N_ROI_COLUMNS

        self.roi_mid_width = roi_width
        self.roi_first_height = roi_height
        self.roi_second_height = roi_height * 2

        # possibly unnecessary
        images = []
        for row in range(0, N_ROI_ROWS):
            for column in range(0, N_ROI_COLUMNS):
                row_height = row * roi_height
                column_width = column * roi_width
                tmp_image = self.current_frame[
                            row_height: (row + 1) * roi_height,
                            column_width:(column + 1) * roi_width
                            ]
                images.append(tmp_image)


# =====================================================================================================================

if __name__ == "__main__":
    bcgr = BackgroundSubtractionModel()
    bcgr.create_background_model()
    # start video file/webcam stream
    cam = cv2.VideoCapture(VIDEO_SOURCE)

    while 1:
        bcgr.detect_fish(cam)

        # if the `q` key is pressed, break from the lop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            log("Pressed 'q' to exit.")
            break
    close_capture_window(cam)
    log("Process finished.")
