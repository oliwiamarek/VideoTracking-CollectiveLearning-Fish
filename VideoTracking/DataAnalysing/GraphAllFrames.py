import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file, get_array_increments, is_not_string


def get_data_from(fileName):
    # type: (str) -> []
    number_of_fish_in_6_roi = [0]
    # reading csv file
    with open(fileName, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        i = 0
        # extracting each data row one by one
        for row in csv_reader:
            if '6' in row[0]:
                number_of_fish_in_6_roi[i] += int(row[1])
            else:
                i += 1
                number_of_fish_in_6_roi.append(0)
        return number_of_fish_in_6_roi


trial = get_data_from(get_csv_file())

blah = len(trial) % 200
if blah > 0:
    del trial[-blah:]

trial_numpy = np.array(trial)
trial_seconds = np.max(trial_numpy.reshape(-1, 200), axis=1)

# plot with various axes scales
plt.figure(1)

plt.plot(trial_seconds, 'r')
plt.axis([0, 150, 0, 20])
# plt.title('manual')

plt.show()

