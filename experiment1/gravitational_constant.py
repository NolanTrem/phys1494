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

# Convert height from mm to cm
data['h (cm)'] = data['h (mm)'] / 10.0

# Group data by height (now in cm) and calculate mean and standard error for each height
grouped_data = data.groupby('h (cm)')
means = grouped_data['ax (m/s^2)'].apply(calculate_mean_and_error).reset_index()

# Split the combined column into separate columns
means[['ax_mean', 'ax_error']] = pd.DataFrame(means['ax (m/s^2)'].tolist(), index=means.index)
del means['ax (m/s^2)']

# Display the values for h, ax_mean, and ax_error
print("Height (h), Mean Acceleration (ax_mean), and Standard Error (ax_error):")
print(means)

# Fit a line to the data
slope, intercept, r_value, p_value, std_err = linregress(means['h (cm)'], means['ax_mean'])

# Display the slope and its standard error
print(f"\nSlope (m): {slope:.5f} with standard error: {std_err:.5f}")

# Display the intercept and its standard error
SE_intercept = std_err * np.sqrt((1/len(means['h (cm)'])) + (np.mean(means['h (cm)'])**2 / sum((means['h (cm)'] - np.mean(means['h (cm)']))**2)))
print(f"Intercept (b): {intercept:.5f} with standard error: {SE_intercept:.5f}")

# Create a best-fit line
best_fit_line = slope * means['h (cm)'] + intercept

# Plotting
plt.figure(figsize=(10, 6))
plt.errorbar(means['h (cm)'], means['ax_mean'], yerr=means['ax_error'], fmt='o', label='Experimental Data', capsize=5)
plt.plot(means['h (cm)'], best_fit_line, '-r', label=f'Best Fit Line (y = {slope:.5f}x + {intercept:.5f})')
plt.title("Acceleration vs Track Height")
plt.xlabel("Track Height (h) in cm")
plt.ylabel("Acceleration (ax) in m/s^2")
plt.legend()
plt.grid(True)
plt.savefig('experiment1/figures/gravitational_acceleration_graph.png')

# Calculate g using the slope and track length
g_estimated = slope * L
sigma_g = std_err * L

print(f"\nEstimated value for g: {g_estimated:.4f} m/s^2 with an uncertainty of σg = {sigma_g:.4f} m/s^2")

data['Delta'] = (data['v1 (m/s)'] ** 2) / (2 * data['ax (m/s^2)'] * data['l2 (m)']) - 1

# Display the Delta values for each trial
print("Delta values for the trials:")
print(data[['Trial #', 'Delta']])