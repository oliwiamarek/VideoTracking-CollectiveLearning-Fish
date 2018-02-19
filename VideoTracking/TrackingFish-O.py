# Otar Akanyeti
# 16 July 2017
# Oliwia Marek
# 18 February 2018
# This program enables the user to digitize fish position manually

import matplotlib.pyplot as plt
import numpy as np
import cv2

# initialize global variables
start_time_minute = 0
start_time_seconds = 1
stop_time_minute = 0
stop_time_seconds = 3
mX, mY = -1, -1
fr, fishX, fishY = [], [], []
save_exp_var = True
locX, locY = np.empty(4), np.zeros(4)


def draw_circle(event, x, y, flags, param):
    global mX, mY
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
        mX, mY = x, y


def calculate_frames(capture, minute, seconds):
    return int((minute * 60 + seconds) * capture.get(5))


def exit_program(capture):
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # TODO Create a "choose file" button instead of fixed input
    cap = cv2.VideoCapture("June28_1.mp4")
    print("width = ", cap.get(3))
    print('height = ', cap.get(4))
    print('frame rate per second = ', '%.2f' % cap.get(5))
    print('number of frames = ', cap.get(7))

    # calculate start and stop frames (normalized between 0 and 1)
    start_frame_no = calculate_frames(cap, start_time_minute, start_time_seconds)
    stop_frame_no = calculate_frames(cap, stop_time_minute, stop_time_seconds)
    print('starting frame number = ', start_frame_no)
    print('stoping frame number ', stop_frame_no)

    # initialize the starting frame of the video object to start_frame_no
    cap.set(1, start_frame_no)

    # create a window
    window_name = 'Fishies'
    cv2.namedWindow(window_name)

    while cap.isOpened():

        # read next frame
        ret, frame = cap.read()

        #TODO get rid of while 1
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

                #TODO refactor
                with open("GOPR2715_exp_var.csv", 'w') as out_file:
                    out_string = "start_time_minute" + ", " + str(start_time_minute) + "\n"
                    out_file.write(out_string)
                    out_string = "start_time_seconds" + ", " + str(start_time_seconds) + "\n"
                    out_file.write(out_string)
                    out_string = "stop_time_minute" + ", " + str(stop_time_minute) + "\n"
                    out_file.write(out_string)
                    out_string = "stop_time_seconds" + ", " + str(stop_time_seconds) + "\n"
                    out_file.write(out_string)
                    out_string = "video width" + ", " + str(cap.get(3)) + "\n"
                    out_file.write(out_string)
                    out_string = "video height" + ", " + str(cap.get(4)) + "\n"
                    out_file.write(out_string)
                    out_string = "frame rate" + ", " + str(cap.get(5)) + "\n"
                    out_file.write(out_string)
                    out_string = "number of frames" + ", " + str(cap.get(7)) + "\n"
                    out_file.write(out_string)
                    out_string = "start frame no" + ", " + str(start_frame_no) + "\n"
                    out_file.write(out_string)
                    out_string = "stop frame no" + ", " + str(stop_frame_no) + "\n"
                    out_file.write(out_string)
                    out_string = "light center x-coordinate" + ", " + str(locX[0]) + "\n"
                    out_file.write(out_string)
                    out_string = "light center y-coordinate" + ", " + str(locY[0]) + "\n"
                    out_file.write(out_string)
                    out_string = "light edge x-coordinate" + ", " + str(locX[1]) + "\n"
                    out_file.write(out_string)
                    out_string = "light edge y-coordinate" + ", " + str(locY[1]) + "\n"
                    out_file.write(out_string)
                    out_string = "food ring center x-coordinate" + ", " + str(locX[2]) + "\n"
                    out_file.write(out_string)
                    out_string = "food ring center y-coordinate" + ", " + str(locY[2]) + "\n"
                    out_file.write(out_string)
                    out_string = "food ring edge x-coordinate" + ", " + str(locX[3]) + "\n"
                    out_file.write(out_string)
                    out_string = "food ring edge y-coordinate" + ", " + str(locY[3]) + "\n"
                    out_file.write(out_string)
                    out_file.close()

        if cap.get(1) > stop_frame_no:
            break

    exit_program(cap)

    # write digitized coordinates into an output file
    with open("GOPR2715_output_data.csv", 'w') as out_file:
        for n in range(len(fr)):
            out_string = ""
            out_string += str(fr[n])
            out_string += ", " + str(fishX[n])
            out_string += ", " + str(fishY[n])
            out_string += "\n"
            out_file.write(out_string)
            out_file.close()

    # visualize coordinates
    plt.figure()
    plt.plot(fr, fishX, 'k')
    plt.xlabel('frame number')
    plt.ylabel('x-coordinate (pixel)')

    plt.figure()
    plt.plot(fr, fishY, 'k')
    plt.xlabel('frame number')
    plt.ylabel('y-coordinate (pixel)')

    plt.figure()
    plt.plot(fishX, fishY, 'k')
    plt.xlabel('x-coordinate (pixel)')
    plt.ylabel('y-coordinate (pixel)')

    plt.show()
