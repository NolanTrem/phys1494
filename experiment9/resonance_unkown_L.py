import matplotlib.pyplot as plt
import numpy as np
import math

# Data for R = 500 Ohm
data_500_ohm_new = np.array([
    [504.2, 14.4], [763.9, 17.2], [904.9, 18], [1040, 18.8], [1161, 18.8],
    [1272, 19.6], [1420, 19.6], [1596, 19.6], [1789, 19.6], [1876, 19.2],
    [2079, 18.8], [2257, 18.8], [2899, 17.2], [3597, 16], [4392, 14.8],
    [5249, 13.2], [6536, 11.2], [8197, 10], [9434, 8.8], [11176, 7.2]
])

# Function to calculate FWHM
def calculate_fwhm(data):
    max_voltage = np.max(data[:, 1])
    half_max_voltage = max_voltage / 2

    # Filter frequencies where voltage >= half_max_voltage
    fwhm_data = data[data[:, 1] >= half_max_voltage]

    # FWHM is the difference between the max and min frequencies in this filtered data
    return np.max(fwhm_data[:, 0]) - np.min(fwhm_data[:, 0])

# Normalize the data to the maximum Vpp
data_500_ohm_new[:, 1] /= np.max(data_500_ohm_new[:, 1])

# Plot settings
plt.figure(figsize=(12, 8))

# Plotting normalized data as points
plt.scatter(data_500_ohm_new[:, 0], data_500_ohm_new[:, 1], color='green', label='R = 500 Ω')

# Additional plot settings
plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized Peak-to-Peak Voltage')
plt.title('Normalized Vpp vs Frequency for R = 500 Ω')
plt.legend()
plt.grid(True)
plt.show()

# Expected and measured resonance frequencies
expected_freq = 1591     # Hz
measured_freq = 1519.25  # Hz

# Capacitance in Farads (500 nF)
C = 500e-9  # Farads

# Calculating the relative error
relative_error = abs((expected_freq - measured_freq) / expected_freq) * 100

# Calculating the inductance L
L = 1 / ((2 * math.pi * measured_freq) ** 2 * C)

# Outputting the results
print(f"Measured Inductance: {L:.5f} H")
print(f"Relative Error: {relative_error:.2f}%")

fwhm_unknown = calculate_fwhm(data_500_ohm_new)
print(f"FWHM: {fwhm_unknown} Hz")
