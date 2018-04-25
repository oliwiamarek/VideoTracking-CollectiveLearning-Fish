import matplotlib.pyplot as plt
import csv
import numpy as np

from config import get_csv_file, get_array_increments, is_not_string

read_rows = []
read_rows_manual = []


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
            read_rows.append(row)

        # get total number of rows
        # print("Total no. of rows: %d" % csv_reader.line_num)

        return number_of_fish


def get_accuracy_from(manual_list, trial_list):
    i = 0
    accuracy_list = []
    while i < len(manual_list):
        diff = manual_list[i] - trial_list[i]
        if diff < 0:
            diff *= 2
        accuracy_list.append(abs(diff))
        i += 1
    return accuracy_list


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


# no test
def create_figure(self, x_axis, y_axis, title, x_label, y_label):
    """
    :type x_axis: List[int]
    :type y_axis: List[int]
    :type title: str
    :type x_label: str
    :type y_label: str
    """
    if is_not_string(title) or is_not_string(x_label) or is_not_string(y_label):
        raise TypeError("Title or labels not strings. Wrong type.")
    plt.figure()
    no_fish = len(self.current_frame_fish_coord)
    for x in xrange(no_fish):
        plt.plot(get_array_increments(x_axis, x, no_fish + 1), get_array_increments(y_axis, x, no_fish + 1))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)


def visualise_coordinates(self):
    self.create_figure(self.all_fish_x_coord, self.all_fish_y_coord, 'X and Y Coordinates', 'y-coordinate (pixel)',
                       'x-coordinate (pixel)')
    # Block=true prevents the graphs from closing immediately
    plt.show(block=True)
