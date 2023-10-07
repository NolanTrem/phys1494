import numpy as np

from bounding_box import BoundingBox

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
    overall_std_dev_x = ((len(data["Radial measurements"]) - 1) * radial_std_dev**2 + bbox.num_points * bbox_std_dev[0]**2) / total_points
    overall_std_dev_y = ((len(data["Radial measurements"]) - 1) * radial_std_dev**2 + bbox.num_points * bbox_std_dev[1]**2) / total_points
    overall_std_dev_x = np.sqrt(overall_std_dev_x)
    overall_std_dev_y = np.sqrt(overall_std_dev_y)

    # Store results
    results[trial] = {
        "Mean Position": (overall_mean_x, overall_mean_y),
        "Standard Deviation": (overall_std_dev_x, overall_std_dev_y)
    }

output = ""
y_lab_manual = [35.12317744, 63.69481605, 57.62550324, 66.77425112]
y_degree_estimate = [29.61330724, 32.31506849, 31.92818004, 32.45342466]
y_computed = [data["Mean Position"][1] for _, data in results.items()]
differences_lab_manual = [computed - manual for computed, manual in zip(y_computed, y_lab_manual)]
differences_degree_estimate = [computed - estimate for computed, estimate in zip(y_computed, y_degree_estimate)]

for i, (trial, data) in enumerate(results.items()):
    output += f"{trial}:\n"
    output += f"  Mean Position: {data['Mean Position']}\n"
    output += f"  Standard Deviation: {data['Standard Deviation']}\n"
    output += f"  Computed y-coordinate: {y_computed[i]:.4f} cm\n"
    output += f"  Difference from y-lab manual formula: {differences_lab_manual[i]:.4f} cm\n"
    output += f"  Difference from y-degree estimate: {differences_degree_estimate[i]:.4f} cm\n\n"

# Print combined output
print(output)
