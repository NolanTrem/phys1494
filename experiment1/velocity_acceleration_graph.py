import os
import numpy as np
import matplotlib.pyplot as plt

# Create the directory if it doesn't exist
directory = 'experiment1/figures/'
if not os.path.exists(directory):
    os.makedirs(directory)
    
# Constants
initial_position = 150  # cm
velocity_left = -0.5    # cm/s
velocity_right = 0.5    # cm/s
time_to_hit_bumper = initial_position / abs(velocity_left)
total_time = 2 * time_to_hit_bumper  # Assuming it returns to the same position

# Time array
times = np.linspace(0, total_time, 1000)

# Displacement and velocity arrays
displacements = []
velocities = []

for t in times:
    if t < time_to_hit_bumper:
        # Moving left
        displacements.append(initial_position + velocity_left * t)
        velocities.append(velocity_left)
    else:
        # Moving right after bouncing
        time_after_bounce = t - time_to_hit_bumper
        displacements.append(initial_position + velocity_left * time_to_hit_bumper + velocity_right * time_after_bounce)
        velocities.append(velocity_right)

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Displacement graph
ax1.plot(times, displacements, label="Displacement")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Displacement (cm)")
ax1.set_title("Displacement vs. Time")
ax1.grid(True)
ax1.legend()

# Velocity graph
ax2.plot(times, velocities, color='r', label="Velocity")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Velocity (cm/s)")
ax2.set_title("Velocity vs. Time")
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig(f'{directory}velocity_acceleration_graph.png')
plt.show()
