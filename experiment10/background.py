import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Data
voltage = np.array([710, 730, 750, 770, 790, 810, 830, 850, 870, 890, 910, 930, 950, 970, 990])
count = np.array([91, 102, 90, 137, 142, 149, 154, 126, 160, 160, 156, 150, 181, 143, 168])

coefficients = np.polyfit(voltage, count, 2)
polynomial = np.poly1d(coefficients)

# Generate y-values for the quadratic line of best fit
line_of_best_fit = polynomial(voltage)

# Plotting Count vs. Voltage with the line of best fit
plt.figure(figsize=(10, 6))
plt.plot(voltage, count, marker='o', linestyle='', color='b', label='Observed Counts')
plt.plot(voltage, line_of_best_fit, linestyle='-', color='r', label='Line of Best Fit')
plt.title('Count Rate vs. Voltage')
plt.xlabel('Voltage (V)')
plt.ylabel('Count Rate')
plt.legend()
plt.grid(True)
plt.show()
