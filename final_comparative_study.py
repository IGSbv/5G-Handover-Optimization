import numpy as np
import matplotlib.pyplot as plt

# --- Load Data ---
rssi_data = np.load('rssi_data_final.npy')

def simulate_with_params(hys, ttt):
    """Simplified version of your controller to test different settings"""
    n_steps, n_users, _ = rssi_data.shape
    current_conn = np.full(n_users, -1)
    ho_count = 0
    
    for t in range(n_steps):
        for u in range(n_users):
            if current_conn[u] == -1:
                current_conn[u] = np.argmax(rssi_data[t,u])
            else:
                serving = rssi_data[t, u, current_conn[u]]
                best_idx = np.argmax(rssi_data[t,u])
                if rssi_data[t, u, best_idx] > (serving + hys):
                    current_conn[u] = best_idx
                    ho_count += 1
    return ho_count

# --- Run Study ---
hys_values = [0, 1, 2, 3, 5, 10]
results = [simulate_with_params(h, 1) for h in hys_values]

# --- Plot Impact ---
plt.figure(figsize=(10, 5))
plt.bar([str(h)+'dB' for h in hys_values], results, color='skyblue', edgecolor='black')
plt.title("Impact of Hysteresis on Total Handovers (The Ping-Pong Effect)")
plt.xlabel("Hysteresis Margin (dB)")
plt.ylabel("Total Number of Handovers")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()