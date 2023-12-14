import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Function to read the data from a file
def read_intensity_linear_position(filename):
    df = pd.read_csv(filename, sep='\t', header=1)
    return df['Linear Position ( m )'], df['Relative Intensity (  )']

# Function to find the positions of maxima
def find_maxima_positions(linear_positions, intensities):
    maxima_positions = []
    for i in range(1, len(intensities) - 1):
        if intensities[i] > intensities[i - 1] and intensities[i] > intensities[i + 1]:
            maxima_positions.append(linear_positions[i])
    return maxima_positions

# Fitting function
def linear_fit(x, m, c):
    return m * x + c

filepaths = [
    # 'experiment5/linearPositionRelativeIntensity_1.txt',
    # 'experiment5/linearPositionRelativeIntensity_2.txt',
    # 'experiment5/linearPositionRelativeIntensity_3.txt',
    'experiment5/linearPositionRelativeIntensity_4.txt',
    'experiment5/linearPositionRelativeIntensity_5.txt',
    'experiment5/linearPositionRelativeIntensity_6.txt',
]

all_maxima_positions = []

# Read data from all files and find maxima
for filepath in filepaths:
    linear_positions, intensities = read_intensity_linear_position(filepath)
    maxima_positions = find_maxima_positions(linear_positions, intensities)
    all_maxima_positions.extend(maxima_positions)

# Assuming the central maximum is at the midpoint of the list
midpoint = len(all_maxima_positions) // 2
order_numbers = list(range(-midpoint, len(all_maxima_positions) - midpoint))

# Fit the data
params, _ = curve_fit(linear_fit, order_numbers, all_maxima_positions)
slope, intercept = params

plt.scatter(order_numbers, all_maxima_positions, label='Data', color='blue')
plt.plot(order_numbers, linear_fit(np.array(order_numbers), slope, intercept), '--', color='red', label=f'Fit: Slope={slope:.4f}, Intercept={intercept:.4f}')
plt.xlabel('Order Number (m)')
plt.ylabel('Position of Maximum (xm)')
plt.legend()
plt.title('Order Number vs. Position of Maximum')
plt.grid(True)
plt.show()

L = .1065  # distance between the slits and the screen in meters
d = 0.25e-3  # separation between the slits in meters

wavelength_estimate = slope * d / L
print(f"Estimated Wavelength: {wavelength_estimate:.10f} m")

# Estimate the slit width using the calculated slope and wavelength
estimated_slit_width = wavelength_estimate * L / slope
print(f"Estimated Slit Width: {estimated_slit_width:.10f} m")