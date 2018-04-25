import matplotlib.pyplot as plt
import os

from GraphAllFrames import get_data_from, squish_to_seconds_from
from config import get_csv_file

FIRST_ROI = 3
SECOND_ROI = 6

'''
===========================================================================
This program creates graph to show comparison of two graphs from two weeks
===========================================================================
'''

if __name__ == "__main__":
    first_file = get_csv_file()
    first_name = os.path.splitext(os.path.basename(first_file))[0]
    second_file = get_csv_file()
    second_name = os.path.splitext(os.path.basename(second_file))[0]

    first_output = get_data_from(first_file, FIRST_ROI)
    second_output = get_data_from(second_file, SECOND_ROI)

    first_output_in_seconds = squish_to_seconds_from(first_output)
    second_output_in_seconds = squish_to_seconds_from(second_output)

    # plot with various axes scales
    plt.figure(1)

    line1, = plt.plot(first_output_in_seconds, 'r', label=first_name)
    line2, = plt.plot(second_output_in_seconds, 'k', label=second_name)
    legend = plt.legend(handles=[line1, line2], loc=1)
    plt.axis([0, 180, 0, 17])
    plt.title("Number of fish around the food ring")
    plt.ylabel("Number of fish")
    plt.xlabel("Time")

    plt.show()

