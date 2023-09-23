import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Load the data
data = pd.read_csv('experiment1/gravitational_acceleration_data.csv')

# Constants
L = 150  # cm

def calculate_mean_and_error(values):
    """
    Calculate the mean and standard error of a set of values.
    """
    mean_val = np.mean(values)
    std_error = np.std(values, ddof=1) / np.sqrt(len(values))
    return mean_val, std_error

# Group data by height and calculate mean and standard error for each height
grouped_data = data.groupby('h (mm)')
means = grouped_data['ax (m/s^2)'].apply(calculate_mean_and_error).reset_index()

# Split the combined column into separate columns
means[['ax_mean', 'ax_error']] = pd.DataFrame(means['ax (m/s^2)'].tolist(), index=means.index)
del means['ax (m/s^2)']

# Fit a line to the data
slope, intercept, r_value, p_value, std_err = linregress(means['h (mm)'], means['ax_mean'])

# Create a best-fit line
best_fit_line = slope * means['h (mm)'] + intercept

# Plotting
plt.figure(figsize=(10, 6))
plt.errorbar(means['h (mm)'], means['ax_mean'], yerr=means['ax_error'], fmt='o', label='Experimental Data', capsize=5)
plt.plot(means['h (mm)'], best_fit_line, '-r', label=f'Best Fit Line (y = {slope:.5f}x + {intercept:.5f})')
plt.title("Acceleration vs Track Height")
plt.xlabel("Track Height (h) in cm")
plt.ylabel("Acceleration (ax) in m/s^2")
plt.legend()
plt.grid(True)
plt.show()

# Calculate g using the slope and track length
g_estimated = slope * L
sigma_g = std_err * L

print(f"Estimated value for g: {g_estimated:.4f} m/s^2 with an uncertainty of σg = {sigma_g:.4f} m/s^2")
