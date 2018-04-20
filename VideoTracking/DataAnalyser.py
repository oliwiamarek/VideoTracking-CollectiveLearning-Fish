import matplotlib.pyplot as plt
import csv

from config import get_csv_file, get_array_increments, is_not_string


def get_data_from(fileName):
    # type: (str) -> []
    read_rows = []
    # reading csv file
    with open(fileName, 'r') as csv_file:
        # creating a csv reader object
        csv_reader = csv.reader(csv_file)

        # extracting each data row one by one
        for row in csv_reader:
            read_rows.append(row)

        # get total number of rows
        print("Total no. of rows: %d" % csv_reader.line_num)

        return read_rows


# x-coordinates of left sides of bars
left = [1, 2, 3, 4, 5]

# heights of bars
height = [10, 24, 36, 40, 5]

filename = get_csv_file()

rows = get_data_from(filename)

# labels for bars
tick_label = ['one', 'two', 'three', 'four', 'five']

# plotting a bar chart
plt.bar(left, height, tick_label=tick_label,
        width=0.8, color=['red', 'green'])

# naming the x-axis
plt.xlabel('x - axis')
# naming the y-axis
plt.ylabel('y - axis')
# plot title
plt.title('My bar chart!')

# function to show the plot
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
