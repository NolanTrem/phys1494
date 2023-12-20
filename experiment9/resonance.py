import matplotlib.pyplot as plt
import numpy as np

# Data for each resistance value
data_50_ohm = np.array([
    [110.9, 0.56], [143.2, 0.72], [186.8, 0.96], [202.7, 1.04], [232.5, 1.2],
    [273.5, 1.44], [369.8, 2.08], [480.7, 2.56], [539.9, 2.72], [581.3, 2.72],
    [730.9, 2.48], [836.1, 2.16], [950.5, 2], [1033, 1.84], [1152, 1.68],
    [1355, 1.36], [1572, 1.2], [2049, 1.04], [2262, 0.96], [3480, 0.72]])

data_10_ohm = np.array([
    [114.6, 0.32], [164.3, 0.4], [202.4, 0.4], [273.5, 0.56], [366, 0.72],
    [414.5, 0.88], [452.8, 0.96], [500, 1.04], [538.7, 1.04], [580, 1.04],
    [666.6, 1.04], [694.4, 0.96], [868, 0.8], [992, 0.72], [1186, 0.56],
    [1534, 0.48], [1805, 0.4], [2688, 0.32], [3233, 0.24], [3704, 0.24]])

data_500_ohm = np.array([
    [112.6, 4.32], [130.4, 4.8], [173.2, 6.16], [199.2, 6.96], [312.7, 9.84],
    [395.5, 11], [470.8, 11.6], [506.1, 11.6], [555.5, 11.6], [599.5, 11.6],
    [688.7, 11.2], [737.6, 11], [896.2, 10.3], [1008, 9.84], [1174, 9.12],
    [1359, 8.4], [1712, 7.36], [2618, 5.52], [3247, 4.72], [3866, 4.08]])

# Normalize the data
data_10_ohm[:, 1] /= np.max(data_10_ohm[:, 1])
data_50_ohm[:, 1] /= np.max(data_50_ohm[:, 1])
data_500_ohm[:, 1] /= np.max(data_500_ohm[:, 1])

# Measured resonant frequencies
measured_resonance = {
    10: 571.325, # Hz
    50: 560.6,   # Hz
    500: 532.975 # Hz
}

# Expected resonance frequency
expected_freq = 581.07  # Hz

def calculate_fwhm_and_uncertainty(data, freq_precision=1):
    max_voltage = np.max(data[:, 1])
    half_max_voltage = max_voltage / 2

    fwhm_data = data[data[:, 1] >= half_max_voltage]
    fwhm = np.max(fwhm_data[:, 0]) - np.min(fwhm_data[:, 0])

    # Uncertainty estimation: twice the frequency precision
    fwhm_uncertainty = 2 * freq_precision
    return fwhm, fwhm_uncertainty


# Function to calculate relative accuracy
def relative_accuracy(measured, expected):
    return abs((measured - expected) / expected) * 100

# Plot settings
plt.figure(figsize=(12, 8))

# Plotting normalized data as points
plt.scatter(data_50_ohm[:, 0], data_50_ohm[:, 1], color='blue', label='R = 50 Ω')
plt.scatter(data_10_ohm[:, 0], data_10_ohm[:, 1], color='red', label='R = 10 Ω')
plt.scatter(data_500_ohm[:, 0], data_500_ohm[:, 1], color='green', label='R = 500 Ω')

# Additional plot settings
plt.xlabel('Frequency (Hz)')
plt.ylabel('Normalized Peak-to-Peak Voltage')
plt.title('Normalized Vpp vs Frequency for Different Resistances')
plt.legend()
plt.grid(True)
plt.show()

# Calculate and print relative accuracy
for R, freq in measured_resonance.items():
    accuracy = relative_accuracy(freq, expected_freq)
    print(f'Relative accuracy for R = {R} Ω: {accuracy:.2f}%')

fwhm_10, unc_10 = calculate_fwhm_and_uncertainty(data_10_ohm)
fwhm_50, unc_50 = calculate_fwhm_and_uncertainty(data_50_ohm)
fwhm_500, unc_500 = calculate_fwhm_and_uncertainty(data_500_ohm)

print(f"FWHM for 10 Ω resistor: {fwhm_10} Hz ± {unc_10} Hz")
print(f"FWHM for 50 Ω resistor: {fwhm_50} Hz ± {unc_50} Hz")
print(f"FWHM for 500 Ω resistor: {fwhm_500} Hz ± {unc_500} Hz")