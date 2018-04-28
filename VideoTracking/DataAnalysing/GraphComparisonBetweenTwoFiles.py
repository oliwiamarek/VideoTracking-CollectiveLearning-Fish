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

from GraphAllFrames import get_data_from, squish_to_seconds_from
from config import get_csv_file, get_name_from_path, smooth

ROI = [5, 6]  # array to store number of region of interest of each of the videos in order
NUMBER_OF_FILES = 2

'''
===========================================================================
This program creates graph to show comparison of two graphs from two weeks
===========================================================================
'''

if __name__ == "__main__":
    filepaths = []  # array to store all filepaths opened
    outputs = []  # array to store all data read from the files
    linetypes = ['k', 'r--', ':', 'g-.']  # types of lines in the plotted graphs

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
        # modifiy the output to make graph smaller
        output = squish_to_seconds_from(outputs[n])
        # create lines and the legend for both outputs
        plt.plot(smooth(output), linetypes[n], label=get_name_from_path(filepaths[n]))
    legend = plt.legend(loc=2)
    plt.axis([0, 120, 0, 17])
    plt.title("Number of fish in ROI with the ring during each experiment")
    plt.ylabel("Number of fish")
    plt.xlabel("Time")

    plt.show()

