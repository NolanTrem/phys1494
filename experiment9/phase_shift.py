import numpy as np
import matplotlib.pyplot as plt
import math

# Constants
L = 0.150  # Inductance in Henries (150mH)
C = 500e-9  # Capacitance in Farads (500nF)
R_values = [10, 50, 500]  # Resistance values in Ohms

# Phase shift data
data_phase_shift = np.array([
    [138, -1.483529864, 7.2, -1.7],
    [343, -0.9467813477, 2.92, -0.44],
    [577.3, -0.07222052077, 1.74, -0.02],
    [1005, -7.180783208, 0.96, -0.84],
    [2000, -11.05840614, 0.5, -0.88]
])

# Phase Shift of the Inductor
data_inductor = np.array([
    [10000, 1.63362818, 0.1, 0.026]
])

# Phase Shift of the Capacitor
data_capacitor = np.array([
    [20, -1.832595715, 48, -14]
])

# Function to calculate phase shift
def calculate_phase_shift(data):
    phase_shifts = []
    for freq, _, total_time, time_diff in data:
        omega = 2 * np.pi * freq
        T_d = total_time / 1000  # Convert ms to s
        t_R_t_d = time_diff / 1000  # Convert ms to s
        phi = (2 * np.pi * t_R_t_d) / T_d
        phase_shifts.append((freq, phi, omega))
    return phase_shifts

# Function to calculate theoretical phase shift
def theoretical_phase_shift(omega, R, L, C):
    tan_phi = (omega * L - 1 / (omega * C)) / R
    return np.arctan(tan_phi)
    

# Calculate phase shifts
measured_phase_shifts = calculate_phase_shift(data_phase_shift)
inductor_phase_shifts = calculate_phase_shift(data_inductor)
capacitor_phase_shifts = calculate_phase_shift(data_capacitor)

# Plot phase shifts
plt.figure(figsize=(12, 8))

# Plotting measured phase shifts
freqs, phases, omegas = zip(*measured_phase_shifts)
plt.plot(freqs, phases, 'o-', label='Measured Phase Shift')

# Plot theoretical phase shifts for different resistors
for R in R_values:
    theoretical_phases = [theoretical_phase_shift(omega, R, L, C) for omega in omegas]
    plt.plot(freqs, theoretical_phases, '--', label=f'Theoretical Phase Shift (R={R} Ω)')

# Adding a horizontal line at zero for reference
plt.axhline(0, color='gray', linestyle='--')

plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase Shift (Radians)')
plt.title('Phase Shift vs Frequency')
plt.legend()
plt.grid(True)
plt.show()

# Print results
print("Measured Phase Shifts (Radians):")
for freq, phase, _ in measured_phase_shifts:
    print(f"Frequency: {freq} Hz, Phase Shift: {phase:.2f} radians")

print("\nPhase Shifts of the Inductor (Radians):")
for freq, phase, _ in inductor_phase_shifts:
    print(f"Frequency: {freq} Hz, Phase Shift: {phase:.2f} radians")

print("\nPhase Shifts of the Capacitor (Radians):")
for freq, phase, _ in capacitor_phase_shifts:
    print(f"Frequency: {freq} Hz, Phase Shift: {phase:.2f} radians")
