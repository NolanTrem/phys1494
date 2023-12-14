import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Gamma particle data
data = np.array([
    [0, 0, 212.4, 30], [0, 0, 227.4, 30], [0, 0, 193.4, 30],
    [0.062, 0.13888, 221.4, 30], [0.062, 0.13888, 185.4, 30], [0.062, 0.13888, 197.4, 30],
    [0.124, 0.27776, 174.4, 30], [0.124, 0.27776, 164.4, 30], [0.124, 0.27776, 165.4, 30],
    [0.186, 0.41664, 121.4, 30], [0.186, 0.41664, 117.4, 30], [0.186, 0.41664, 139.4, 30],
    [0.248, 0.55552, 93.4, 30], [0.248, 0.55552, 116.4, 30], [0.248, 0.55552, 94.4, 30],
    [0.31, 0.6944, 93.4, 30], [0.31, 0.6944, 99.4, 30], [0.31, 0.6944, 102.4, 30]
])


# Group data by thickness and calculate average count rate and its standard deviation
unique_thicknesses = np.unique(data[:, 1])
avg_ln_counts = []
std_devs = []

for thickness in unique_thicknesses:
    counts_at_thickness = data[data[:, 1] == thickness, 2]
    corrected_counts = counts_at_thickness / data[data[:, 1] == thickness, 3]  # Correct for time
    ln_corrected_counts = np.log(corrected_counts)
    avg_ln_counts.append(np.mean(ln_corrected_counts))
    std_devs.append(np.std(ln_corrected_counts))

# Convert lists to numpy arrays for plotting
avg_ln_counts = np.array(avg_ln_counts)
std_devs = np.array(std_devs)

# Linear regression on the averaged data
slope, intercept, _, _, std_err = linregress(unique_thicknesses, avg_ln_counts)

# Plotting with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(unique_thicknesses, avg_ln_counts, yerr=std_devs, fmt='o', linestyle='', color='b', label='Averaged Data')
plt.plot(unique_thicknesses, slope * unique_thicknesses + intercept, color='r', label='Line of Best Fit')  # Line of best fit
plt.title('Logarithmic Analysis of Gamma Ray Attenuation in Lead')
plt.xlabel('Lead Absorber Thickness (cm)')
plt.ylabel('Ln(Count Rate)')
plt.legend()
plt.grid(True)
plt.show()

# Absorption coefficient (μ) is the negative of the slope
absorption_coefficient = -slope
print(f"Linear Absorption Coefficient (μ): {absorption_coefficient:.3f} cm^-1")
