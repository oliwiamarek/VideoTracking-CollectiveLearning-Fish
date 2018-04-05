import argparse
import numpy as np
import cv2

# https://pdfs.semanticscholar.org/8a1f/27fd371eceb8654b735502b810d2094e420b.pdf
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# http://layer0.authentise.com/how-to-track-objects-with-stationary-background.html
# https://medium.com/machine-learning-world/tutorial-making-road-traffic-counting-app-based-on-computer-vision-and-opencv-166937911660

# ===============================================
VIDEO_SOURCE = "ExampleVid/week4.mp4"  # path to video
DEBUG = True  # used to print debug logs
WAITING_FRAMES = 500  # default number of frames used to calculate bcgr model
MIN_AREA_SIZE = 1300  # default minimum area size for contours
THRESHOLD = 0.01  # default value of threshold used in bcgr subtraction average calculation
X_COORD = []
Y_COORD = []


# ===============================================
# Used for printing out things for debugging purposes
def log(s):
    if DEBUG:
        print s


def construct_argument_parser():
    # construct the argument parser and parse the arguments
    # look https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
    ap = argparse.ArgumentParser()
    ap.add_argument("-a", "--min-area", type=int, default=MIN_AREA_SIZE, help="minimum area size for contours")
    ap.add_argument("-f", "--waiting-frames", type=int, default=WAITING_FRAMES,
                    help="number of frames used to calculate bcgr model")
    ap.add_argument("-t", "--threshold", type=float, default=THRESHOLD,
                    help="threshold used in bcgr subtraction average calculation")
    return vars(ap.parse_args())


def create_background_model(arguments):
    noWaitingFrames = arguments["waiting_frames"]
    print("Calculating the background model. Please wait {0} seconds".format(noWaitingFrames))
    global bcgrModel
    # start video file/webcam stream
    camera = cv2.VideoCapture(VIDEO_SOURCE)
    ret, frame = camera.read()
    movingAverage = np.float32(frame)
    for i in range(noWaitingFrames):
        grabbed, currentFrame = camera.read()

        # if frame could not be grabbed, we reached the end of video
        if not grabbed:
            break

        cv2.accumulateWeighted(currentFrame, movingAverage, arguments["threshold"])
        # do the drawing stuff
        bcgrModel = cv2.convertScaleAbs(movingAverage)
        log("Frame number: {0} done successfully.".format(i))
    print("Model calculated")
    camera.release()

    # show the background model
    createWindow("Background Model", bcgrModel)
    log("Opened background model window for: {0}".format(bcgrModel))

    return bcgrModel


def createWindow(title, variable):
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, variable)


def detect_fish(arguments, background_model):
    print("Start Fish detection.")
    # start video file/webcam stream
    camera = cv2.VideoCapture(VIDEO_SOURCE)
    while 1:
        grabbed, currentFrame = camera.read()

        # if frame could not be grabbed, we reached the end of video
        if not grabbed:
            break

        # convert to greyscale and blur it
        differenceImage = cv2.absdiff(background_model, currentFrame)
        gray = cv2.cvtColor(differenceImage, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        log("Successfully converted to greyscale and blurred.")

        # compute the absolute difference between the current frame and background frame
        thresh = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the threshold image to fill in holes, then find contours on threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)
        im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        log("Successfully found contours.")

        # loop over the contours
        for c in contours:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < arguments["min_area"]:
                continue

            # compute the bounding box for the contour, draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            X_COORD.append(x)
            Y_COORD.append(y)
            cv2.circle(currentFrame, (x + w / 2, y + h / 2), 5, (0, 255, 0), -1)

        log("X coord: {0}".format(X_COORD))
        log("Y coord: {0}".format(Y_COORD))
        del X_COORD[:]
        del Y_COORD[:]

        createWindow("Frame", currentFrame)
        createWindow("Foreground", thresh)
        createWindow("Frame Delta", differenceImage)

        # if the `q` key is pressed, break from the lop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            log("Pressed 'q' to exit.")
            break
    from MainProgram import close_capture_window
    close_capture_window(camera)
    log("Process finished.")


# =====================================================================================================================

if __name__ == "__main__":
    args = construct_argument_parser()
    backgroundModel = create_background_model(args)
    detect_fish(args, backgroundModel)
