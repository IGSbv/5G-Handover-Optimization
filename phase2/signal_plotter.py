import numpy as np
import matplotlib.pyplot as plt

# --- 1. Load Data ---
try:
    rssi_data = np.load('rssi_data_final.npy')
    n_steps, n_users, n_towers = rssi_data.shape
except FileNotFoundError:
    print("Error: 'rssi_data_final.npy' not found.")
    exit()

# --- 2. Select a User to Analyze ---
USER_ID = 0  # Change this to see different user profiles (0 to 99)

# --- 3. Plotting ---
plt.figure(figsize=(12, 6))
time_axis = np.arange(n_steps)

plt.plot(time_axis, rssi_data[:, USER_ID, 0], label='Cell A (200, 200)', alpha=0.8)
plt.plot(time_axis, rssi_data[:, USER_ID, 1], label='Cell B (800, 200)', alpha=0.8)
plt.plot(time_axis, rssi_data[:, USER_ID, 2], label='Cell C (500, 800)', alpha=0.8)

# Add a "Sensitivity Threshold" line
plt.axhline(y=-110, color='r', linestyle='--', label='Min Sensitivity (-110 dBm)')

plt.title(f"RSSI Profile for User {USER_ID} over Time")
plt.xlabel("Time Step (Seconds)")
plt.ylabel("Signal Strength (dBm)")
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)

# Save the plot for your documentation
plt.savefig(f'user_{USER_ID}_rssi_profile.png')
plt.show()