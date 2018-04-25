import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file

ROI_VALUE = 5

'''
===========================================================================
FUNCTIONS
===========================================================================
'''


def get_data_from(fileName, roi):
    # type: (str, int) -> []
    number_of_fish_in_6_roi = [0]
    # reading csv file
    with open(fileName, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        i = 0
        # extracting each data row one by one
        for row in csv_reader:
            if str(roi) in row[0]:
                number_of_fish_in_6_roi[i] += int(row[1])
            else:
                i += 1
                number_of_fish_in_6_roi.append(0)
        return number_of_fish_in_6_roi


def squish_to_seconds_from(trial_list):
    # type: ([]) -> []
    # To make it present it better, take max from 200 frames.
    # if it is not dividable by 200, delete number of items equivalent to the modulus.
    modulus = len(trial_list) % 200
    if modulus > 0:
        del trial_list[-modulus:]

    # Able to take maximum of n items by using numpy array
    trial_numpy = np.array(trial_list)
    return np.max(trial_numpy.reshape(-1, 200), axis=1)


'''
===========================================================================
MAIN
===========================================================================
'''
if __name__ == "__main__":
    trial = get_data_from(get_csv_file(), ROI_VALUE)

    trial_seconds = squish_to_seconds_from(trial)

    # plot with various axes scales
    plt.figure(1)

    plt.plot(trial_seconds, 'r')
    plt.axis([0, 180, 0, 18])
    plt.title("Number of fish around food ring during duration of the video")
    plt.ylabel("Number of fish")
    plt.xlabel("Time")

    plt.show()

