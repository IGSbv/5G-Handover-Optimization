import numpy as np
import matplotlib.pyplot as plt

# --- 1. Load Physics Data ---
rssi_data = np.load('rssi_data_final.npy') # (Time, User, Tower)
n_steps, n_users, n_towers = rssi_data.shape

# --- 2. Network Parameters ---
HYSTERESIS = 3.0    # dB margin to prevent frequent switching
TTT_STEPS = 2       # Time-To-Trigger (consecutive steps needed)
CELL_CAPACITY = 40  # Max users per tower
MIN_SENSITIVITY = -110.0 # dBm threshold for "Dropped" calls

def run_network_simulation():
    # Track current connection for each user (-1 means disconnected)
    current_connections = np.full(n_users, -1, dtype=int)
    # Track how long a new tower has been "better"
    ttt_counter = np.zeros(n_users, dtype=int)
    target_tower = np.full(n_users, -1, dtype=int)
    
    # Metrics to track
    handover_count = 0
    dropped_calls = np.zeros(n_steps)
    tower_load = np.zeros((n_steps, n_towers))

    for t in range(n_steps):
        current_tower_usage = np.zeros(n_towers)
        
        for u in range(n_users):
            user_rssi = rssi_data[t, u]
            best_tower = np.argmax(user_rssi)
            
            # Initial Connection Logic
            if current_connections[u] == -1:
                if user_rssi[best_tower] > MIN_SENSITIVITY:
                    current_connections[u] = best_tower
            
            # Handover Logic with Hysteresis
            else:
                serving_rssi = user_rssi[current_connections[u]]
                target_rssi = user_rssi[best_tower]
                
                # Check if a different tower is significantly better
                if best_tower != current_connections[u] and target_rssi > (serving_rssi + HYSTERESIS):
                    if best_tower == target_tower[u]:
                        ttt_counter[u] += 1
                    else:
                        target_tower[u] = best_tower
                        ttt_counter[u] = 1
                    
                    # If TTT met and capacity allows, perform Handover
                    if ttt_counter[u] >= TTT_STEPS:
                        if current_tower_usage[best_tower] < CELL_CAPACITY:
                            current_connections[u] = best_tower
                            handover_count += 1
                            ttt_counter[u] = 0
                else:
                    ttt_counter[u] = 0 # Reset if signal drops
            
            # Check for Dropped Calls
            if current_connections[u] != -1:
                if user_rssi[current_connections[u]] < MIN_SENSITIVITY:
                    current_connections[u] = -1
                else:
                    current_tower_usage[current_connections[u]] += 1

        tower_load[t] = current_tower_usage
        dropped_calls[t] = np.sum(current_connections == -1)

    return handover_count, tower_load, dropped_calls

# --- 3. Execution & Performance Analysis ---
ho_total, load_history, drop_history = run_network_simulation()

print(f"Total Handovers: {ho_total}")
print(f"Average Dropped Users: {np.mean(drop_history):.2f}")

# Plot Tower Load over time
plt.figure(figsize=(10, 5))
plt.plot(load_history[:, 0], label='Cell A Load')
plt.plot(load_history[:, 1], label='Cell B Load')
plt.plot(load_history[:, 2], label='Cell C Load')
plt.axhline(y=CELL_CAPACITY, color='r', linestyle='--', label='Max Capacity')
plt.title("Network Traffic & Load Balancing")
plt.xlabel("Time Step")
plt.ylabel("Number of Connected Users")
plt.legend()
plt.show()