import matplotlib.pyplot as plt

"""
===========================================================================
This program creates a graph of maximum number of fish in the region of 
interest where the food ring was in each of the weeks in first and second 
experiment.
===========================================================================
"""

# plot with various axes scales
plt.figure(1)

# plot the maximum number with week number.
plt.plot([8, 11, 12, 16, 17], [1, 2, 3, 4, 5], 'r^', [8, 11, 12, 16, 17], [1, 2, 3, 4, 5], 'r',
         [11, 12, 15, 13, 15], [1, 2, 3, 4, 5], 'bs', [11, 12, 15, 13, 15], [1, 2, 3, 4, 5], 'b')
plt.axis([6, 18, 0, 6])
plt.title("Maximum number of fish around food ring between buzzer and food dropping")
plt.ylabel("Number of fish")
plt.xlabel("Weeks")

plt.show()
