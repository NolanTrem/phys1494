"""
Analysis of current as a function of curvature
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

voltage = [100, 100, 100, 200, 200, 200, 300, 300, 300, 400, 400, 400, 500, 500, 500]
current = [1, 0.86, 1.19, 1, 1.28, 1.64, 1.78, 2.03, 1.59, 1.84, 2.07, 1.66, 2.06, 1.86, 2.63]
current_high = [1.09, 0.94, 1.28, 1.06, 1.36, 1.76, 1.9, 2.18, 1.68, 1.95, 2.2, 1.75, 2.18, 1.96, 2.83]
current_low = [0.89, 0.77, 1.12, 0.94, 1.21, 1.54, 1.68, 1.9, 1.51, 1.75, 1.95, 1.58, 1.96, 1.78, 2.47]
diameter = [0.075, 0.08, 0.06, 0.11, 0.09, 0.07, 0.08, 0.07, 0.09, 0.09, 0.08, 0.1, 0.09, 0.1, 0.07]

unique_voltages = sorted(set(voltage))

# Adjusted function
def plot_current_vs_inv_radius(voltage, current, current_high, current_low, diameter):
    # Convert diameter to radius
    radius = [d / 2 for d in diameter]
    
    # Calculate 1/r
    inv_radius = [1 / r for r in radius]
    
    # Calculate error for each current value using absolute difference
    errors = [abs(high - low) / 2 for high, low in zip(current_high, current_low)]
    
    # Plot I against 1/r for each voltage
    unique_voltages = sorted(set(voltage))
    
    plt.figure(figsize=(10, 6))
    
    for v in unique_voltages:
        indices = [i for i, x in enumerate(voltage) if x == v]
        
        sorted_data = sorted([(inv_radius[i], current[i], errors[i]) for i in indices], key=lambda x: x[0])
        sorted_inv_radius, sorted_current, sorted_errors = zip(*sorted_data)
        
        plt.errorbar(sorted_inv_radius,
                    sorted_current,
                    yerr=sorted_errors,
                    label=f'V={v}V', marker='o', linestyle='-')

    plt.xlabel('1/r (1/m)')
    plt.ylabel('Current (A)')
    plt.title('Current (A) vs 1/r (m^-1)')
    plt.legend()
    plt.grid(True)
    plt.show()

def weighted_least_squares_fit(voltage, inv_radius, current, current_high, current_low):
    results = []
    for v in unique_voltages:
        # Extracting data corresponding to the voltage
        indices = [i for i, x in enumerate(voltage) if x == v]
        v_inv_radius = [inv_radius[i] for i in indices]
        v_current = [current[i] for i in indices]
        
        # Calculate errors and weights
        v_errors = [abs(current_high[i] - current_low[i]) / 2 for i in indices]
        weights = [1 / e**2 for e in v_errors]
        
        # Weighted linear regression
        slope, intercept = np.polyfit(v_inv_radius, v_current, 1, w=weights)
        
        # Standard errors for slope and intercept
        y_fit = [slope*x + intercept for x in v_inv_radius]
        residuals = [y_fit[i] - v_current[i] for i in range(len(v_current))]
        residual_sum_squares = sum([r**2 for r in residuals])
        variance = residual_sum_squares / (len(v_inv_radius) - 2)
        std_error_slope = (variance / sum([(x - np.mean(v_inv_radius))**2 for x in v_inv_radius]))**0.5
        std_error_intercept = (variance * sum([x**2 for x in v_inv_radius]) / (len(v_inv_radius) * sum([(x - np.mean(v_inv_radius))**2 for x in v_inv_radius])))**0.5
        
        results.append({
            'Voltage (V)': v,
            'Slope A': slope,
            'Intercept D': intercept,
            'σA': std_error_slope,
            'σD': std_error_intercept
        })

    return pd.DataFrame(results)

# Call the function with the updated data
plot_current_vs_inv_radius(voltage, current, current_high, current_low, diameter)

# Create a DataFrame with the data
data = pd.DataFrame({
    'Voltage (V)': voltage,
    'Current (A)': current,
    'Current High (A)': current_high,
    'Current Low (A)': current_low,
    'Diameter (m)': diameter,
    'Radius (m)': [d/2 for d in diameter],
    '1/Radius (1/m)': [1/(d/2) for d in diameter]
})

# Call the function to plot the data
plot_current_vs_inv_radius(voltage, current, current_high, current_low, diameter)

# Create a DataFrame with the data
data = pd.DataFrame({
    'Voltage (V)': voltage,
    'Current (A)': current,
    'Current High (A)': current_high,
    'Current Low (A)': current_low,
    'Diameter (m)': diameter,
    'Radius (m)': [d/2 for d in diameter],
    '1/Radius (1/m)': [1/(d/2) for d in diameter]
})

# Compute the weighted least squares results and display them
results_df = weighted_least_squares_fit(voltage, data['1/Radius (1/m)'].values, data['Current (A)'].values, current_high, current_low)
print(results_df)

# Constants
C = 0.0008047  # T A^-1

# Extracting the values from the results dataframe
voltages = results_df['Voltage (V)'].values
slopes_A = results_df['Slope A'].values
errors_A = results_df['σA'].values

# Calculating e/m and its uncertainty for each estimate
em_values = [2*V / (A**2 * C**2) for V, A in zip(voltages, slopes_A)]
sigma_em_values = [((-4*V) / (A**3 * C**2) * sigma_A)**2 for V, A, sigma_A in zip(voltages, slopes_A, errors_A)]

em_values, np.sqrt(sigma_em_values)

print(f'e/m = {np.mean(em_values)} ± {np.sqrt(np.mean(sigma_em_values))}')