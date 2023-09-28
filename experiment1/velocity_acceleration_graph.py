import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_graphs(velocity_left, velocity_right, label_prefix, save_name):
    """
    Generates displacement and velocity graphs for a given set of left and right velocities.
    """

    # Constants
    initial_position = 150  # cm
    time_to_hit_bumper = initial_position / abs(velocity_left)
    total_time = 2 * time_to_hit_bumper  # Assuming it returns to the same position

    # Time array
    times = np.linspace(0, total_time, 1000)

    # Displacement and velocity arrays
    displacements = []
    velocities = []

    for t in times:
        if t < time_to_hit_bumper:
            # Moving left towards the bumper
            displacements.append(initial_position + velocity_left * t)
            velocities.append(velocity_left)
        else:
            # Moving right after bouncing
            time_after_bounce = t - time_to_hit_bumper
            displacements.append(velocity_right * time_after_bounce)
            velocities.append(velocity_right)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Displacement graph
    ax1.plot(times, displacements, label=f"{label_prefix} Displacement")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Displacement (cm)")
    ax1.set_title(f"{label_prefix} Displacement vs. Time")
    ax1.grid(True)
    ax1.legend()

    # Velocity graph
    ax2.plot(times, velocities, color="r", label=f"{label_prefix} Velocity")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (cm/s)")
    ax2.set_title(f"{label_prefix} Velocity vs. Time")
    ax2.grid(True)
    ax2.legend()

    ax1.set_xticks([])
    ax2.set_xticks([])

    plt.tight_layout()
    plt.savefig(f"{directory}{save_name}.png")
    plt.show()


def generate_real_graph(velocity_left, velocity_right, label_prefix, save_name):
    """
    Generates a more realistic graph with interpolated velocity during collision.
    """

    # Constants
    initial_position = 150  # cm
    time_to_hit_bumper = initial_position / abs(velocity_left)
    total_time = 2 * time_to_hit_bumper

    # Time array
    times = np.linspace(0, total_time, 1000)

    # Displacement and velocity arrays
    displacements = []
    velocities = []

    # Define a small time window for interpolation around the collision
    interpolation_window = 0.05 * time_to_hit_bumper  # 5% of the time to hit the bumper

    midpoint_velocity = (velocity_left + velocity_right) / 2

    for t in times:
        if t < time_to_hit_bumper - interpolation_window:
            # Moving left before approaching the bumper
            displacements.append(initial_position + velocity_left * t)
            velocities.append(velocity_left)
        elif t < time_to_hit_bumper + interpolation_window:
            # Using the midpoint velocity during the interpolation window
            displacements.append(displacements[-1] + midpoint_velocity * (times[1] - times[0]))
            velocities.append(midpoint_velocity)
        else:
            # Moving right after bouncing
            time_after_bounce = t - (time_to_hit_bumper + interpolation_window)
            displacements.append(
                displacements[-1] + velocity_right * (times[1] - times[0])
            )
            velocities.append(velocity_right)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Displacement graph
    ax1.plot(times, displacements, '--', label=f"{label_prefix} Displacement")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Displacement (cm)")
    ax1.set_title(f"{label_prefix} Displacement vs. Time")
    ax1.grid(True)
    ax1.legend()

    # Velocity graph with dashed line for interpolation
    ax2.plot(times, velocities, "r--", label=f"{label_prefix} Velocity")
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Velocity (cm/s)")
    ax2.set_title(f"{label_prefix} Velocity vs. Time")
    ax2.grid(True)
    ax2.legend()

    ax1.set_xticks([])
    ax2.set_xticks([])

    plt.tight_layout()
    plt.savefig(f"{directory}{save_name}.png")
    plt.show()

# Create the directory if it doesn't exist
directory = "experiment1/figures/"
if not os.path.exists(directory):
    os.makedirs(directory)

# Ideal data
generate_graphs(-0.5, 0.5, "Ideal", "ideal_velocity_acceleration_graph")


# Real data from CSV
data = pd.read_csv("experiment1/data.csv")
v_final_average = data['v final'].mean()
v_initial_average = data['v initial'].mean()

generate_real_graph(v_final_average, v_initial_average, "Real", "real_velocity_acceleration_graph")