import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Data Organization
data = {
    "10 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [10, 7, 6, 5.5, 5, 4.5, 4, 3, 2.5, 2],
        "current_2": [10, 8, 7, 5.5, 5, 4.5, 4, 3, 2.5, 2]
    },
    "20 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [9, 8.5, 8, 7.5, 7, 6.5, 6, 5.5, 5, 5],
        "current_2": [9, 8.5, 8, 7, 6.5, 6, 6, 5.5, 5, 5]
    },
    "30 µF": {
        "time": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "current_1": [9.5, 9, 9, 8.5, 8, 7, 7, 6.5, 6, 6],
        "current_2": [9.5, 9, 8.5, 8, 7.5, 7.5, 7, 6.5, 6.5, 6]
    }
}

# Averaging Currents and Transforming Data
averaged_data = {}
for capacitance, values in data.items():
    averaged_data[capacitance] = {
        "time": np.array(values["time"]),
        "average_current": np.mean([values["current_1"], values["current_2"]], axis=0)
    }

# Linear Regression Analysis and Plotting
plt.figure(figsize=(12, 8))

regression_results = {}
for capacitance, values in averaged_data.items():
    ln_current = np.log(values["average_current"])
    time = values["time"]
    transformed_uncertainty = 0.5 / values["average_current"]  # Transforming uncertainties

    # Linear Regression
    slope, intercept, r_value, p_value, std_err = linregress(time, ln_current)
    regression_results[capacitance] = {
        "tau": -1 / slope,
        "tau_err": std_err / slope**2
    }

    # Plotting
    plt.errorbar(time, ln_current, yerr=transformed_uncertainty, fmt='o', label=f'{capacitance} ln(Current)')
    plt.plot(time, slope*time + intercept, label=f'{capacitance} Regression Line')

     # Adding τ value with error in a yellow box
    plt.text(8, slope*8 + intercept - 0.5, f'τ ({capacitance}) = {regression_results[capacitance]["tau"]:.2f} ± {regression_results[capacitance]["tau_err"]:.2f} s', 
             fontsize=12, bbox=dict(facecolor='yellow', alpha=0.5))

# Finalizing Plot
plt.title('ln(Current) vs Time with Linear Regression')
plt.xlabel('Time (s)')
plt.ylabel('ln(Current)')
plt.legend()
plt.grid(True)
plt.show()

# Outputting Regression Results
for capacitance, results in regression_results.items():
    print(f"{capacitance}: τ = {results['tau']:.2f} ± {results['tau_err']:.2f} s")

# Calculating and Comparing Ratios of Tau
def calculate_ratio(tau1, tau1_err, tau2, tau2_err):
    ratio = tau1 / tau2
    ratio_err = ratio * np.sqrt((tau1_err / tau1)**2 + (tau2_err / tau2)**2)
    return ratio, ratio_err

tau_10, tau_10_err = regression_results["10 µF"]["tau"], regression_results["10 µF"]["tau_err"]
tau_20, tau_20_err = regression_results["20 µF"]["tau"], regression_results["20 µF"]["tau_err"]
tau_30, tau_30_err = regression_results["30 µF"]["tau"], regression_results["30 µF"]["tau_err"]

ratio_30_20, ratio_30_20_err = calculate_ratio(tau_30, tau_30_err, tau_20, tau_20_err)
