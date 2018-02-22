# Otar Akanyeti
# 16 July 2017
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position manually

import matplotlib.pyplot as plt
import numpy as np
import cv2
import tkFileDialog
import os

# initialize global variables
mX, mY = -1, -1
fr, fishX, fishY = [], [], []
save_exp_var = True
locX, locY = np.empty(4), np.zeros(4)


def draw_circle(event, x, y, flags, param):
    global mX, mY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        mX, mY = x, y


def calculate_frames(capture, seconds):
    return int(seconds * capture.get(5))


def exit_program(capture):
    capture.release()
    cv2.destroyAllWindows()


def select_dipole_and_food():
    global mX, mY
    count = 0
    while 1:

        cv2.imshow(window_name, frame)  # show it

        cv2.putText(frame, 'Click for Light Source and Cylinder', (130, 180),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                    2)  # , cv2.LINE_AA) # display the frame number

        cv2.setMouseCallback(window_name, draw_circle)
        if cv2.waitKey(1) % 0xFF == ord('n'):
            if mX > -1 and mY > -1:
                locX[count] = mX
                locY[count] = mY
                mX, mY = -1, -1

                count += 1
                if count == 1:
                    cv2.putText(frame, 'Light center = ' + str(locX[0]) + ', ' + str(locY[0]), (130, 230),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                2)  # , cv2.LINE_AA) # display the frame number
                elif count == 2:
                    cv2.putText(frame, 'Light edge = ' + str(locX[1]) + ', ' + str(locY[1]), (130, 280),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                2)  # , cv2.LINE_AA) # display the frame number
                elif count == 3:
                    cv2.putText(frame, 'Food ring center = ' + str(locX[2]) + ', ' + str(locY[2]),
                                (130, 330),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                2)  # , cv2.LINE_AA) # display the frame number
                elif count == 4:
                    cv2.putText(frame, 'Food ring edge edge = ' + str(locX[3]) + ', ' + str(locY[3]),
                                (130, 380),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                                2)  # , cv2.LINE_AA) # display the frame number

                if count > 3:
                    break
            else:
                cv2.putText(frame, 'Please first click on a point', (830, 180), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 0, 255), 2)  # , cv2.LINE_AA)  # display the frame number


def visualise_coordinates(fr, fishX, fishY):
    # visualize coordinates
    plt.figure()
    plt.plot(fr, fishX, 'k')
    plt.title('X Coordinates visualisation')
    plt.xlabel('frame number')
    plt.ylabel('x-coordinate (pixel)')
    plt.figure()
    plt.plot(fr, fishY, 'k')
    plt.title('Y Coordinates visualisation')
    plt.xlabel('frame number')
    plt.ylabel('y-coordinate (pixel)')
    plt.figure()
    plt.plot(fishX, fishY, 'k')
    plt.title('X and Y Coordinates')
    plt.ylabel('y-coordinate (pixel)')
    plt.xlabel('x-coordinate (pixel)')
    # Block=true prevents the graphs from closing immediately
    plt.show(block=True)


def write_to_output_file():
    with open('output_' + filename + ".csv", 'w') as output_file:
        for n in range(len(fr)):
            output_string = ""
            output_string += str(fr[n])
            output_string += ", " + str(fishX[n])
            output_string += ", " + str(fishY[n])
            output_string += "\n"
            variable_file.write(output_string)
    output_file.close()


# TODO Delete?
def write_to_variable_file():
    global variable_file
    with open('variables_' + filename + ".csv", 'w') as variable_file:
        out_string = "video width" + ", " + str(cap.get(3)) + "\n"
        variable_file.write(out_string)
        out_string = "video height" + ", " + str(cap.get(4)) + "\n"
        variable_file.write(out_string)
        out_string = "frame rate" + ", " + str(cap.get(5)) + "\n"
        variable_file.write(out_string)
        out_string = "number of frames" + ", " + str(cap.get(7)) + "\n"
        variable_file.write(out_string)
        variable_file.close()


if __name__ == "__main__":
    filepath = ""
    # ask for video file
    while not filepath:
        # restrict to only videos
        filepath = tkFileDialog.askopenfilename(title="Choose a video file", filetypes=[("Video Files", "*.avi *.mp4")])
    # get name from path
    filename = os.path.splitext(os.path.basename(filepath))[0]

    cap = cv2.VideoCapture(filepath)
    print("width = ", cap.get(3))
    print('height = ', cap.get(4))
    print('frame rate per second = ', '%.2f' % cap.get(5))
    print('number of frames = ', cap.get(7))

    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(cap, 1)
    stop_frame_no = calculate_frames(cap, 2)
    print('starting frame number = ', start_frame_no)
    print('stoping frame number ', stop_frame_no)

    # initialize the starting frame of the video object to start_frame_no
    cap.set(1, start_frame_no)

    # create a window
    window_name = 'Fishies'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while cap.isOpened():

        # read next frame
        ret, frame = cap.read()

        if ret:  # check if the frame has been read properly
            while 1:
                cv2.imshow(window_name, frame)  # show it
                cv2.putText(frame, 'frame no = ' + str(cap.get(1)), (130, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)  # , cv2.LINE_AA) # display the frame number
                cv2.setMouseCallback(window_name, draw_circle)
                if cv2.waitKey(1) % 0xFF == ord('n'):
                    if mX > -1 and mY > -1:
                        fr.append(cap.get(1))
                        fishX.append(mX)
                        fishY.append(mY)
                        mX, mY = -1, -1
                        break
                    else:
                        cv2.putText(frame, 'Please first click on a point', (830, 130), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (0, 0, 255), 2)  # , cv2.LINE_AA)  # display the frame number

            if save_exp_var:
                save_exp_var = False
                # select_dipole_and_food()

                # write_to_variable_file()

        if cap.get(1) > stop_frame_no:
            break

    exit_program(cap)

    # write digitized coordinates into an output file
    write_to_output_file()

    visualise_coordinates(fr, fishX, fishY)
