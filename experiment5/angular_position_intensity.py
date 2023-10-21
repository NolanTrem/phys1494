import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_intesity_angular_position(filename):
    df = pd.read_csv(filename, sep='\t', header=0)
    return df['Angular Position ( deg )'], df['Relative Intensity (  )']

def normalize_phase(angular_positions, intensities):
    # 1. Discard data above 360 degrees
    valid_indices = angular_positions <= 360
    angular_positions = angular_positions[valid_indices]
    intensities = intensities[valid_indices]
    
    # 2. Find the angular position corresponding to the highest intensity
    max_intensity_index = intensities.idxmax()
    phase_offset = angular_positions[max_intensity_index]
    
    # 3. Subtract this value from all angular positions
    normalized_angular_positions = angular_positions - phase_offset
    
    # 4. Adjust the values to ensure they are between 0 and 360 degrees
    normalized_angular_positions = normalized_angular_positions % 360
    
    return normalized_angular_positions, intensities

def calculate_avg_and_std(*trials):
    # Convert tuples to DataFrame objects
    dfs = [pd.DataFrame({'Angular Position ( deg )': trial[0], 'Relative Intensity (  )': trial[1]}) for trial in trials]
    
    # Combine all trials into one dataframe
    all_data = pd.concat(dfs, axis=0)
    
    # Sample 20 points between 0 and 360
    sample_points = np.linspace(0, 360, 20)
    avg_intensities = []
    std_intensities = []
    
    # Define a window around each sample point (e.g., 9 degrees on either side)
    window = 9
    
    for point in sample_points:
        subset = all_data[(all_data['Angular Position ( deg )'] >= point - window) & (all_data['Angular Position ( deg )'] <= point + window)]
        avg_intensities.append(subset['Relative Intensity (  )'].mean())
        std_intensities.append(subset['Relative Intensity (  )'].std())
    
    return sample_points, avg_intensities, std_intensities

plt.figure(figsize=(10, 6))

trial_1 = read_intesity_angular_position('experiment5/intensityAngularPosition_1.txt')
normalized_trial_1 = normalize_phase(trial_1[0], trial_1[1])

trial_2 = read_intesity_angular_position('experiment5/intensityAngularPosition_2.txt')
normalized_trial_2 = normalize_phase(trial_2[0], trial_2[1])

trial_3 = read_intesity_angular_position('experiment5/intensityAngularPosition_3.txt')
normalized_trial_3 = normalize_phase(trial_3[0], trial_3[1])

# Calculate average and standard deviation
angular_positions, avg_intensities, std_intensities = calculate_avg_and_std(normalized_trial_1, normalized_trial_2, normalized_trial_3)

plt.errorbar(angular_positions, avg_intensities, yerr=std_intensities, fmt='o', color='blue', ecolor='red', capsize=5)
plt.title('Graph of Angular Position vs. Average Relative Intensity')
plt.xlabel('Angular Position (deg)')
plt.ylabel('Relative Intensity')
plt.grid(True)
plt.show()