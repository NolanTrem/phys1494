import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Given data
L = 0.1024  # in meters
data = {
    "I": [4, 4, 4, 4, 4, 3.5, 3.5, 3.5, 3.5, 3.5, 3, 3, 3, 3, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2, 2, 2, 2, 2],
    "iL": [0.0256, 0.0512, 0.0768, 0.1024, 0.128, 0.0256, 0.0512, 0.0768, 0.1024, 0.128, 0.0256, 0.0512, 0.0768, 0.1024, 0.128, 0.0256, 0.0512, 0.0768, 0.1024, 0.128, 0.0256, 0.0512, 0.0768, 0.1024, 0.128],
    "F=mg": [0.003924, 0.0138321, 0.0168732, 0.0211896, 0.0227592, 0.003924, 0.0080442, 0.0118701, 0.0170694, 0.0210915, 0.0036297, 0.0061803, 0.0101043, 0.0141264, 0.0161865, 0.0036297, 0.0051993, 0.0089271, 0.0120663, 0.0152055, 0.0022563, 0.0043164, 0.0069651, 0.0091233, 0.012753]
}

# Extracting unique I values for individual plots
unique_I = np.unique(data["I"])

# Plotting iL against F=mg for each I
plt.figure(figsize=(12, 8))
for current in unique_I:
    idx = [i for i, x in enumerate(data["I"]) if x == current]
    x_values = [data["iL"][i] for i in idx]
    y_values = [data["F=mg"][i] for i in idx]
    plt.scatter(x_values, y_values, label=f"I = {current} mA")
    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
    plt.plot(x_values, [slope*x + intercept for x in x_values], linestyle='--')

plt.xlabel('iL (mA*m)')
plt.ylabel('F = mg (N)')
plt.legend()
plt.title('iL vs F=mg for various I values')
plt.grid(True)
plt.show()

# Calculating B for each I setting
B_values = []
B_errors = []
for current in unique_I:
    idx = [i for i, x in enumerate(data["I"]) if x == current]
    x_values = [data["iL"][i] for i in idx]
    y_values = [data["F=mg"][i] for i in idx]
    slope, intercept, r_value, p_value, std_err = linregress(x_values, y_values)
    B_values.append(slope)
    B_errors.append(std_err)

# Plotting B against I
plt.figure(figsize=(12, 8))
plt.errorbar(unique_I, B_values, yerr=B_errors, fmt='o-', label='Measured B values')
plt.xlabel('I (mA)')
plt.ylabel('B (T)')
plt.title('B vs I with error bars')
plt.grid(True)
plt.legend()
plt.show()

B_values, B_errors
