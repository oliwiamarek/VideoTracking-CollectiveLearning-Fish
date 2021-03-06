#
# This program creates a graph of maximum number of fish in the region of  interest where the food ring was in each
# of the weeks in first and second experiment. The variables are hard coded and were recorded manually.
#

import matplotlib.pyplot as plt

plt.figure(1)

# plot the maximum number with week number.
line1, = plt.plot([1, 2, 3, 4, 5], [8, 11, 12, 16, 17], 'r^', label='first experiment')
plt.plot([1, 2, 3, 4, 5], [8, 11, 12, 16, 17], 'r')
line2, = plt.plot([1, 2, 3, 4, 5], [11, 12, 15, 13, 15], 'bs', label='second experiment')
plt.plot([1, 2, 3, 4, 5], [11, 12, 15, 13, 15], 'b')
plt.legend(loc='upper center', ncol=2)
plt.axis([0, 6, 6, 18])
plt.title("Maximum number of fish around food ring between buzzer and food dropping")
plt.ylabel("Number of fish")
plt.xlabel("Weeks")

plt.show()
