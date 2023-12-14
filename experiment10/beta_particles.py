import numpy as np
import matplotlib.pyplot as plt

# Background radiation correction (counts per minute)
background_count_rate = 46.6 # per minute

# Data for Thickness of Absorbers and Count Rate
# Including all your provided data
data = np.array([
    # Thickness in cm, Count, Time of Count in seconds
    [0.01016, 112, 15], [0.01016, 128, 15], [0.01016, 128, 15],
    [0.02032, 87, 15], [0.02032, 79, 15], [0.02032, 80, 15],
    [0.03048, 71, 15], [0.03048, 65, 15], [0.03048, 62, 15],
    [0.04064, 54, 15], [0.04064, 54, 15], [0.04064, 43, 15],
    [0.0508, 29, 15], [0.0508, 37, 15], [0.0508, 40, 15],
    [0.06096, 27, 15], [0.06096, 31, 15], [0.06096, 32, 15],
    [0.07112, 18, 15], [0.07112, 26, 15], [0.07112, 22, 15],
    [0.01016, 248, 30], [0.01016, 249, 30], [0.01016, 234, 30],
    [0.02032, 174, 30], [0.02032, 162, 30], [0.02032, 179, 30],
    [0.03048, 131, 30], [0.03048, 137, 30], [0.03048, 116, 30],
    [0.04064, 103, 30], [0.04064, 91, 30], [0.04064, 105, 30],
    [0.0508, 82, 30], [0.0508, 70, 30], [0.0508, 67, 30],
    [0.06096, 70, 30], [0.06096, 52, 30], [0.06096, 63, 30],
    [0.07112, 58, 30], [0.07112, 56, 30], [0.07112, 50, 30]
])

# Calculating average counts and standard deviation for each thickness
unique_thicknesses = np.unique(data[:, 0])
avg_counts = []
std_devs = []

for thickness in unique_thicknesses:
    counts_at_thickness = data[data[:, 0] == thickness, 1]
    avg_counts.append(np.mean(counts_at_thickness))
    std_devs.append(np.std(counts_at_thickness))

# Correcting for background radiation and converting to counts per minute
corrected_counts = [(count - background_count_rate * (time / 60)) * (60 / time) for count, time in zip(avg_counts, data[:, 2])]
corrected_errors = [std_dev * (60 / time) for std_dev, time in zip(std_devs, data[:, 2])]

# Plotting Corrected Count Rate vs. Aluminum Absorber Thickness with error bars
plt.figure(figsize=(10, 6))
plt.errorbar(unique_thicknesses, corrected_counts, yerr=corrected_errors, fmt='o', linestyle='-', color='b')
plt.title('Beta Particle Attenuation in Aluminum Absorbers')
plt.xlabel('Absorber Thickness (cm)')
plt.ylabel('Corrected Count Rate (counts/minute)')
plt.grid(True)
plt.show()

# Estimate Maximum Beta Energy
density_Al = 2.702  # g/cm^3
range_max = unique_thicknesses[-1]  # Maximum range from the graph
energy_max = ((range_max / (0.412 * density_Al)) ** (1/1.29))  # MeV

# Expected value and standard deviation of maximum energy for Thallium-204
expected_energy = 0.765  # MeV
energy_std_dev = np.std([(range_val / (0.412 * density_Al)) ** (1/1.29) for range_val in unique_thicknesses])

# Calculate the number of standard deviations away from the expected value
num_std_devs = (energy_max - expected_energy) / energy_std_dev

print(f"Estimated Maximum Energy of Beta Particles: {energy_max:.3f} MeV")
print(f"Number of standard deviations from expected value: {num_std_devs:.2f}")