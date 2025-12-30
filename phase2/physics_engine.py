import numpy as np

# --- 1. Load Data from Phase 1 ---
try:
    positions = np.load('user_positions_advanced.npy')
    n_steps, n_users, _ = positions.shape
except FileNotFoundError:
    print("Error: 'user_positions_advanced.npy' not found. Run Phase 1 first!")
    exit()

# --- 2. Simulation Constants ---
TOWER_LOCATIONS = np.array([
    [200, 200],  # Cell A
    [800, 200],  # Cell B
    [500, 800]   # Cell C
])

P_TX = 30.0        # Transmit Power (dBm)
N_EXP = 3.5        # Path Loss Exponent (Urban)
SIGMA = 6.0        # Shadowing Standard Deviation (dB)
REF_DISTANCE = 1.0 # Reference distance (meters)
L0 = 40.0          # Path loss at reference distance (dB)

# --- 3. The Signal Strength Calculator ---
def get_rssi_matrix(positions):
    """
    Computes RSSI for every user from every tower over all time steps.
    Output Shape: (n_steps, n_users, 3_towers)
    """
    n_towers = TOWER_LOCATIONS.shape[0]
    rssi_out = np.zeros((n_steps, n_users, n_towers))

    for t in range(n_steps):
        for u in range(n_users):
            u_pos = positions[t, u]
            
            for tow_idx in range(n_towers):
                t_pos = TOWER_LOCATIONS[tow_idx]
                
                # Calculate Euclidean Distance
                dist = np.linalg.norm(u_pos - t_pos)
                dist = max(dist, 0.1) # Prevent log of zero
                
                # Path Loss calculation
                path_loss = L0 + 10 * N_EXP * np.log10(dist / REF_DISTANCE)
                
                # Add Random Shadowing (The "Real-World" Noise)
                shadowing = np.random.normal(0, SIGMA)
                
                # Resulting RSSI
                rssi_out[t, u, tow_idx] = P_TX - path_loss + shadowing
                
    return rssi_out

# --- 4. Run and Save ---
print("Calculating Signal Strengths (RSSI) for all users...")
rssi_data = get_rssi_matrix(positions)

np.save('rssi_data_final.npy', rssi_data)
print(f"Success! Saved RSSI matrix of shape {rssi_data.shape} to 'rssi_data_final.npy'.")

# --- 5. Quick Check ---
avg_rssi = np.mean(rssi_data)
print(f"Average RSSI across the simulation: {avg_rssi:.2f} dBm")