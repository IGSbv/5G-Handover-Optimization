import numpy as np

# --- 1. Load Student A's Data ---
positions = np.load('user_positions_advanced.npy') # Shape: (Time, User, XY)

# --- 2. Define Network Environment ---
TOWER_LOCATIONS = np.array([
    [200, 200],  # Tower 0 (Cell A)
    [800, 200],  # Tower 1 (Cell B)
    [500, 800]   # Tower 2 (Cell C)
])
P_TX = 30  # Transmit power in dBm (Small Cell)
N_VAL = 3.5 # Path loss exponent (Urban environment)
SIGMA = 6.0 # Standard deviation for Shadowing (The "Noise")

def calculate_rssi(user_pos):
    """Calculates RSSI from all 3 towers for a single user position"""
    rssi_values = []
    for tower in TOWER_LOCATIONS:
        # Euclidean Distance
        d = np.linalg.norm(user_pos - tower)
        d = max(d, 1) # Avoid log(0)
        
        # Log-Normal Shadowing Model
        path_loss = 20 * np.log10(d) + (10 * N_VAL * np.log10(d/10))
        shadowing = np.random.normal(0, SIGMA)
        
        rssi = P_TX - path_loss + shadowing
        rssi_values.append(rssi)
    return rssi_values

# --- 3. Process the entire timeline ---
n_steps, n_users, _ = positions.shape
rssi_matrix = np.zeros((n_steps, n_users, 3))

for t in range(n_steps):
    for u in range(n_users):
        rssi_matrix[t, u] = calculate_rssi(positions[t, u])

# --- 4. Export for Student C ---
np.save('rssi_data_final.npy', rssi_matrix)
print("Physics simulation complete. RSSI data saved for Student C.")