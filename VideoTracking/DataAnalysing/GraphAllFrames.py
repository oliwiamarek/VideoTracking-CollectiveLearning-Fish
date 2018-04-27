#
# This program takes an output file with fish numbers in each ROI and plots a graph of how many fish are around the
# food ring in the duration of the whole video (about 120 seconds)
#

import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file, get_name_from_path

ROI_VALUE = 5  # which Region of Interest we want to take into account

'''
===========================================================================
FUNCTIONS
===========================================================================
'''


# read csv file
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
    modulus = len(trial_list) % 300
    if modulus > 0:
        del trial_list[-modulus:]

    # Able to take average of n items by using numpy array
    trial_numpy = np.array(trial_list)
    return np.max(trial_numpy.reshape(-1, 300), axis=1)


'''
===========================================================================
MAIN
===========================================================================
'''
if __name__ == "__main__":
    # get path and name of the files
    filepath = get_csv_file()
    filename = get_name_from_path(filepath)
    trial = get_data_from(filepath, ROI_VALUE)

    trial_seconds = squish_to_seconds_from(trial)

    # plot with various axes scales
    plt.figure(1)

    plt.plot(trial_seconds, 'r', label=filename)
    plt.axis([0, 120, 0, 18])
    plt.title("Number of fish around food ring during duration of the video")
    plt.ylabel("Number of fish")
    plt.xlabel("Time (s)")
    plt.legend()

    plt.show()
