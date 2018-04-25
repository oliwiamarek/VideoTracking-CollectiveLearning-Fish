import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file, get_array_increments, is_not_string

"""
===========================================================================
FUNCTIONS
===========================================================================
"""


def get_data_from(fileName):
    # type: (str) -> []
    number_of_fish = [0]
    # reading csv file
    with open(fileName, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        i = 0
        previous = ' '
        # extracting each data row one by one
        for row in csv_reader:
            if row[0] == ' ':
                i += 1
                number_of_fish.append(0)
            elif row[0] == previous:
                number_of_fish[i] += 1
            else:
                number_of_fish[i] += 1
            previous = row[0]

        return number_of_fish


def get_accuracy_from(list_manual, list_trial):
    i = 0
    list_accuracy = []
    while i < len(list_manual):
        diff = list_manual[i] - list_trial[i]
        if diff < 0:
            diff *= 2
        list_accuracy.append(abs(diff))
        i += 1
    return list_accuracy


"""
===========================================================================
MAIN
===========================================================================
"""
if __name__ == "__main__":
    manual = get_data_from(get_csv_file())
    trial = get_data_from(get_csv_file())

    blah = len(manual) % 5
    if blah > 0:
        del manual[-blah:]

    length = abs(len(manual) - len(trial))
    if length != 0:
        del trial[-length:]

    accuracy_list = get_accuracy_from(manual, trial)
    average_accuracy = sum(accuracy_list) / float(len(accuracy_list))
    print average_accuracy

    trial_numpy = np.array(trial)
    trial_list = np.max(trial_numpy.reshape(-1, 5), axis=1)

    manual_numpy = np.array(manual)
    manual_list = np.mean(manual_numpy.reshape(-1, 5), axis=1)

    accuracy_list = get_accuracy_from(manual_list, trial_list)
    average_accuracy = sum(accuracy_list) / float(len(accuracy_list))
    print average_accuracy

    # plot with various axes scales
    plt.figure(1)

    plt.plot(trial_list, 'r', manual_list, 'b')
    plt.axis([0, 24, 5, 30])
    plt.title('manual')

    plt.show()
