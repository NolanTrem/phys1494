import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Organizing the discharging data
discharging_data = {
    "10 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [9, 7, 6.5, 6, 5, 4.5, 4, 3, 2.5, 2],
        "current_2": [8.5, 8, 7.5, 5, 4.5, 4, 3.5, 3.5, 3, 2]
    },
    "20 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 4.5],
        "current_2": [9, 8, 7.5, 7, 6.5, 6.5, 6, 5, 5, 4.5]
    },
    "30 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [9.5, 9, 8.5, 8, 7.5, 7, 7, 7, 6.5, 6],
        "current_2": [10, 9, 8.5, 8, 7.5, 7.5, 7, 6.5, 6.5, 6]
    }
}

# Averaging the currents for discharging data
averaged_discharging_data = {}
for capacitance, values in discharging_data.items():
    averaged_discharging_data[capacitance] = {
        "time": np.array(values["time"]),
        "average_current": np.mean([values["current_1"], values["current_2"]], axis=0)
    }

# Linear Regression Analysis and Plotting for Discharging Data
plt.figure(figsize=(12, 8))

discharging_regression_results = {}
for capacitance, values in averaged_discharging_data.items():
    ln_current = np.log(values["average_current"])
    time = values["time"]
    transformed_uncertainty = 0.5 / values["average_current"]  # Transforming uncertainties

    # Linear Regression
    slope, intercept, r_value, p_value, std_err = linregress(time, ln_current)
    discharging_regression_results[capacitance] = {
        "tau": -1 / slope,
        "tau_err": std_err / slope**2
    }

    # Plotting
    plt.errorbar(time, ln_current, yerr=transformed_uncertainty, fmt='o', label=f'{capacitance} ln(Current)')
    plt.plot(time, slope*time + intercept, label=f'{capacitance} Regression Line')

    # Adding τ value with error in a yellow box
    plt.text(8, slope*8 + intercept - 0.5, f'τ ({capacitance}) = {discharging_regression_results[capacitance]["tau"]:.2f} ± {discharging_regression_results[capacitance]["tau_err"]:.2f} s', 
             fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5))

# Finalizing Plot
plt.title('ln(Current) vs Time for Discharging with Linear Regression')
plt.xlabel('Time (s)')
plt.ylabel('ln(Current)')
plt.legend()
plt.grid(True)
plt.show()

# Outputting Regression Results for Discharging
for capacitance, results in discharging_regression_results.items():
    print(f"{capacitance} (Discharging): τ = {results['tau']:.2f} ± {results['tau_err']:.2f} s")

