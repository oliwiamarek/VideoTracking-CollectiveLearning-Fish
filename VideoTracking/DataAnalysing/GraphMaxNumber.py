#
# This program creates a graph of maximum number of fish in the region of  interest where the food ring was in each
# of the weeks in first and second experiment.
#

import matplotlib.pyplot as plt

# plot with various axes scales
plt.figure(1)

# plot the maximum number with week number.
plt.plot([1, 2, 3, 4, 5], [8, 11, 12, 16, 17], 'r^', [1, 2, 3, 4, 5], [8, 11, 12, 16, 17], 'r',
         [1, 2, 3, 4, 5], [11, 12, 15, 13, 15], 'bs', [1, 2, 3, 4, 5], [11, 12, 15, 13, 15], 'b')
plt.axis([0, 6, 6, 18])
plt.title("Maximum number of fish around food ring between buzzer and food dropping")
plt.ylabel("Number of fish")
plt.xlabel("Weeks")

plt.show()
