import numpy as np
import matplotlib.pyplot as plt

from bounding_box import BoundingBox

g = 9.81  # Acceleration due to gravity (m/s^2)

# Data for the trials
trials = {
    "Trial 1": {
        "Radial measurements": [82, 77, 52, 50, 40, 40],
        "Bounding Box": {
            "points": 14,
            "corners": [(-4, 50), (7, 50), (-4, 42), (7, 42)]
        }
    },
    "Trial 2": {
        "Radial measurements": [37, 32, 31, 23, 26],
        "Bounding Box": {
            "points": 15,
            "corners": [(-26, 19), (-22, 19), (-26, 10), (-22, 10)]
        }
    },
    "Trial 3": {
        "Radial measurements": [65, 59, 62, 62, 64, 64, 59, 46, 56, 55],
        "Bounding Box": {
            "points": 10,
            "corners": [(40, 36), (44, 36), (40, 32), (44, 32)]
        }
    },
    "Trial 4": {
        "Radial measurements": [55, 63, 60, 58, 58, 47, 48, 63, 60, 61, 56, 59, 60, 62, 52, 54],
        "Bounding Box": {
            "points": 4,
            "corners": [(45, 33), (49, 33), (45, 29), (49, 29)]
        }
    }
}

provided_data = {
    'Trial 1 (metal)': {'h1': 1.24, 'h2': 1.183, 'h3': 1.125, 'D': 0.274, 'L': 0.292, 'v0': 0.7393, 'x_lab_manual': 0.3512},
    'Trial 2 (metal)': {'h1': 1.29, 'h2': 1.146, 'h3': 1.111, 'D': 0.28, 'L': 0.292, 'v0': 1.3288, 'x_lab_manual': 0.6369},
    'Trial 1 (plastic)': {'h1': 1.314, 'h2': 1.128, 'h3': 1.092, 'D': 0.283, 'L': 0.292, 'v0': 1.2014, 'x_lab_manual': 0.5763},
    'Trial 2 (plastic)': {'h1': 1.334, 'h2': 1.114, 'h3': 1.086, 'D': 0.287, 'L': 0.292, 'v0': 1.3856, 'x_lab_manual': 0.6677}
}

# Calculate expected x and its uncertainty
expected_x = {}
for trial, data in provided_data.items():
    h1 = data['h1']
    h2 = data['h2']
    h3 = data['h3']
    D = data['D']
    L = data['L']
    v0 = data['v0']
    
    x = v0 * (D / L) * (v0 - (h2 - h3) / L + np.sqrt(((v0 - (h2 - h3)) / L)**2 + 2 * g * h2))
    expected_x[trial] = x

# Analyze each trial
results = {}

for trial, data in trials.items():
    # Calculate mean and std dev for radial measurements
    radial_mean = np.mean(data["Radial measurements"])
    radial_std_dev = np.std(data["Radial measurements"])

    # Calculate bounding box mean and std dev
    bbox = BoundingBox(data["Bounding Box"]["corners"][0], data["Bounding Box"]["corners"][2], data["Bounding Box"]["points"])
    bbox_mean = bbox.mean
    bbox_std_dev = bbox.std_dev

    # Calculate overall mean and std dev incorporating bounding box data
    total_points = len(data["Radial measurements"]) + bbox.num_points
    overall_mean_x = (np.sum(data["Radial measurements"]) + bbox.num_points * bbox_mean[0]) / total_points
    overall_mean_y = (np.sum(data["Radial measurements"]) + bbox.num_points * bbox_mean[1]) / total_points
    overall_std_dev_x = np.sqrt(((len(data["Radial measurements"]) - 1) * radial_std_dev**2 + bbox.num_points * bbox_std_dev[0]**2) / total_points)
    overall_std_dev_y = np.sqrt(((len(data["Radial measurements"]) - 1) * radial_std_dev**2 + bbox.num_points * bbox_std_dev[1]**2) / total_points)

    # Store results
    results[trial] = {
        "Mean Position": (overall_mean_x, overall_mean_y),
        "Standard Deviation": (overall_std_dev_x, overall_std_dev_y)
    }

output = ""
x_lab_manual = [35.12317744, 63.69481605, 57.62550324, 66.77425112]
x_degree_estimate = [29.61330724, 32.31506849, 31.92818004, 32.45342466]
x_computed = [data["Mean Position"][1] for _, data in results.items()]
differences_lab_manual = [computed - manual for computed, manual in zip(x_computed, x_lab_manual)]
differences_degree_estimate = [computed - estimate for computed, estimate in zip(x_computed, x_degree_estimate)]

trial_names = list(results.keys())
mean_positions_x = [data["Mean Position"][0] for _, data in results.items()]
mean_positions_z = [data["Mean Position"][1] for _, data in results.items()]
std_devs_x = [data["Standard Deviation"][0] for _, data in results.items()]
std_devs_z = [data["Standard Deviation"][1] for _, data in results.items()]

fig, ax = plt.subplots(figsize=(12, 8))

# For each trial
for trial, data in trials.items():
    # Extract all measurements
    measurements = data["Radial measurements"]
    
    # For bounding box points, use the mean of the bounding box as the measurement
    bbox = BoundingBox(data["Bounding Box"]["corners"][0], data["Bounding Box"]["corners"][2], data["Bounding Box"]["points"])
    bbox_mean_x, bbox_mean_y = bbox.mean
    measurements += [bbox_mean_x] * bbox.num_points  # Adding mean x value for each bounding box point
    
    # The y-error for each point will be the overall std dev of the trial
    y_error = results[trial]["Standard Deviation"][0]
    
    # Plotting each point for the trial
    ax.errorbar([trial] * len(measurements), measurements, yerr=y_error, fmt='o', capsize=5, elinewidth=1, label=f"{trial} measurements")

ax.set_ylabel('Position (cm)')
ax.set_title('Ball Landing Position with Standard Deviation')
plt.xticks(rotation=45)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
ax.legend()
plt.tight_layout()
plt.show()
