import matplotlib.pyplot as plt
import csv

from config import get_csv_file


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
