import argparse
import cv2

# https://pdfs.semanticscholar.org/8a1f/27fd371eceb8654b735502b810d2094e420b.pdf
# https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# http://layer0.authentise.com/how-to-track-objects-with-stationary-background.html

# construct the argument parser and parse the arguments
# look https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--min-area", type=int, default=1000, help="minimum area size")
args = vars(ap.parse_args())

# first frame of the video file/webcam stream
firstFrame = None
camera = cv2.VideoCapture('ExampleVid/week4.mp4')

while 1:
    ret, frame = camera.read()

    # if frame could not be grabbed, we reached the end of video
    if not ret:
        break

    # convert to greyscale and blur it
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    '''ASSUMPTION - first frame no movement '''

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue

    # compute the absolute difference between the current frame and first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    im2, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in contours:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour, draw it on the frame, and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Thresh", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Frame Delta", cv2.WINDOW_NORMAL)
    cv2.imshow("Frame", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break
camera.release()
cv2.destroyAllWindows()
