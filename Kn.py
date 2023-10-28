import math

# Constants
k = 1.38e-23  # Boltzmann constant, J/K
T = 293  # Assumed room temperature, K
P = 1e4  # Pressure, Pa
# Constants for oxygen
d_oxygen = 0.346e-9  # Effective diameter of oxygen molecules, m
d_atomic_oxygen = 0.120e-9
# Calculate Knudsen number
L = 1e-5  # Reference length, m


# Temperature range
T_range = list(range(1100, 2001, 100))


# Calculate Knudsen number for each temperature
Kn_values = [(k * T) / (math.sqrt(2) * math.pi * d_atomic_oxygen**2 * P) / L for T in T_range]
print(Kn_values)