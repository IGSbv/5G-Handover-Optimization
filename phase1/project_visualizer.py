import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- Configuration ---
DATA_FILE = 'user_positions_advanced.npy'
AREA_SIZE = 1000  # 1km x 1km box
ANIMATION_SPEED = 50 # Lower number = faster animation (interval in milliseconds)

# Define Tower Locations (Must match Student B's script exactly)
TOWER_LOCATIONS = np.array([
    [200, 200],  # Tower A
    [800, 200],  # Tower B
    [500, 800]   # Tower C
])

# --- 1. Load Data ---
try:
    # shape: (n_steps, n_users, 2)
    history_data = np.load(DATA_FILE)
    n_steps, n_users, _ = history_data.shape
    print(f"Loaded data for {n_users} users over {n_steps} time steps.")
except FileNotFoundError:
    print(f"ERROR: Could not find {DATA_FILE}. Run the mobility engine first.")
    exit()

# --- 2. Setup the Visualization Figure ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, AREA_SIZE)
ax.set_ylim(0, AREA_SIZE)
ax.set_title(f"5G Cluster Simulation: {n_users} Mobile Agents")
ax.set_xlabel("X Coordinate (meters)")
ax.set_ylabel("Y Coordinate (meters)")
ax.grid(True)

# --- 3. Plot Static Elements (Towers) ---
# Plot towers as large red triangles ('r^')
tower_plot = ax.plot(TOWER_LOCATIONS[:, 0], TOWER_LOCATIONS[:, 1], 
                     'r^', markersize=15, markeredgecolor='k', label='5G Small Cells')

# Add labels to towers
labels = ['Cell A', 'Cell B', 'Cell C']
for i, txt in enumerate(labels):
    ax.annotate(txt, (TOWER_LOCATIONS[i, 0]+20, TOWER_LOCATIONS[i, 1]+20), 
                fontsize=12, color='red')

# Initialize the scatter plot for moving users (blue dots)
user_scatter = ax.scatter([], [], c='blue', s=15, alpha=0.6, label='Mobile Users')
ax.legend(loc='upper right')

# --- 4. Define the Animation Update Function ---
def update_frame(step_idx):
    """
    This function runs for every frame of the animation.
    It grabs the user positions at 'step_idx' and updates the plot.
    """
    # Get positions for all users at this specific time step
    current_positions = history_data[step_idx, :, :]
    
    # Update the scatter plot data
    user_scatter.set_offsets(current_positions)
    
    # Update title to show progression
    ax.set_title(f"5G Cluster Simulation - Time Step: {step_idx}/{n_steps}")
    
    return user_scatter,

# --- 5. Run Animation ---
# blit=True makes it run faster by only redrawing changed parts
ani = FuncAnimation(fig, update_frame, frames=n_steps, 
                    interval=ANIMATION_SPEED, blit=True, repeat=True)

print("Starting animation window...")
plt.show()