#
# This program creates a graph from two files containing information about number of fish in each ROI. It plots a
# graph showing the comparison between the files.
# User has to first change the variables ROI and NUMBER_OF_FILES.
# ROI corresponds to which region of interest do we want to consider in each of the videos.
# First experiment: 3rd ROI
# Second experiment: 6th ROI
# Third experiment: 5th ROI
#

import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file, get_name_from_path, smooth

'''
===========================================================================
VARIABLES 
===========================================================================
'''
ROI = [6, 3, 2]  # array to store number of region of interest of each of the videos in order
NUMBER_OF_FILES = 3

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


def print_max_number_between_buzzer_and_food_in(full_list, file_name):
    list_copy = full_list.copy()
    s = slice(60, 70)
    array = list_copy[s]
    print("Maximum value during the buzzer vibration in file '{0}' is: {1}".format(file_name, np.max(array)))


'''
===========================================================================
MAIN
===========================================================================
'''

if __name__ == "__main__":
    filepaths = []  # array to store all filepaths opened
    outputs = []  # array to store all data read from the files
    linetypes = ['k', 'r--', ':', 'g-.', 'c']  # types of lines in the plotted graphs

    # for each of the files collect the data
    for n in range(NUMBER_OF_FILES):
        # get path of the files
        filepath = get_csv_file()
        filepaths.append(filepath)
        # get data from the file
        the_output = get_data_from(filepath, ROI[n])
        outputs.append(the_output)

    plt.figure(1)

    # for each of the files plot the data collected
    for n in range(NUMBER_OF_FILES):
        filename = get_name_from_path(filepaths[n])
        # modifiy the output to make graph smaller
        output = squish_to_seconds_from(outputs[n])
        print_max_number_between_buzzer_and_food_in(output, filename)
        # create lines and the legend for both outputs
        plt.plot(smooth(output), linetypes[n], label='ROI {0}'.format(ROI[n]))
    legend = plt.legend(loc=2)
    plt.axis([0, 120, 0, 17])
    plt.title("Number of fish in ROIs in: {0}".format(filename))
    plt.ylabel("Number of fish")
    plt.xlabel("Time")

    plt.show()
