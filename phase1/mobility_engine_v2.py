import numpy as np
import matplotlib.pyplot as plt

class MobilityEngine:
    def __init__(self, n_users=100, area_size=1000, dt=1.0):
        self.n_users = n_users
        self.area_size = area_size
        self.dt = dt
        
        # Gauss-Markov Memory Level (0 = Random, 1 = Constant velocity)
        # 0.85 means the user mostly maintains their current direction/speed
        self.alpha = 0.85 
        
        # Initializing user states
        self.pos = np.random.uniform(0, area_size, (n_users, 2))
        self.speed = np.random.uniform(1, 5, n_users)  # m/s
        self.angle = np.random.uniform(0, 2 * np.pi, n_users)
        
        # Mean values to "pull" the randomness back to reality
        self.mean_speed = 1.5  # Average walking speed
        self.mean_angle = np.pi # General drift direction
        
    def update_step(self):
        # Gauss-Markov update formulas
        # New Speed = alpha * Old_Speed + (1-alpha) * Mean_Speed + Noise
        speed_noise = np.random.normal(0, 1, self.n_users)
        self.speed = (self.alpha * self.speed + 
                      (1 - self.alpha) * self.mean_speed + 
                      np.sqrt(1 - self.alpha**2) * speed_noise)
        
        # New Angle = alpha * Old_Angle + (1-alpha) * Mean_Angle + Noise
        angle_noise = np.random.normal(0, 0.2, self.n_users)
        self.angle = (self.alpha * self.angle + 
                      (1 - self.alpha) * self.mean_angle + 
                      np.sqrt(1 - self.alpha**2) * angle_noise)
        
        # Update Coordinates
        self.pos[:, 0] += self.speed * np.cos(self.angle) * self.dt
        self.pos[:, 1] += self.speed * np.sin(self.angle) * self.dt
        
        # Boundary Handling: Reflect off walls
        for i in range(self.n_users):
            if self.pos[i, 0] < 0 or self.pos[i, 0] > self.area_size:
                self.angle[i] = np.pi - self.angle[i]
            if self.pos[i, 1] < 0 or self.pos[i, 1] > self.area_size:
                self.angle[i] = -self.angle[i]
        
        self.pos = np.clip(self.pos, 0, self.area_size)
        return self.pos.copy()

# --- Execution & Export ---
engine = MobilityEngine(n_users=100)
n_steps = 500
full_history = []

for _ in range(n_steps):
    full_history.append(engine.update_step())

# Convert to 3D array: [Time, UserID, Coordinate]
history_array = np.array(full_history)

# Save for Student B
np.save('user_positions_advanced.npy', history_array)
print("Simulation complete. Data saved to 'user_positions_advanced.npy'.")
data = np.load('user_positions_advanced.npy')

# To see the position of User #5 at Time Step #100:
# data[time_step, user_id]
x, y = data[100, 5]
print(f"User 5 is at X: {x:.2f}, Y: {y:.2f}")
# Visual Verification for first 2 users
plt.figure(figsize=(8, 8))
plt.plot(history_array[:, 0, 0], history_array[:, 0, 1], label="User A (Walking)")
plt.plot(history_array[:, 1, 0], history_array[:, 1, 1], label="User B (Walking)")
plt.title("Advanced Gauss-Markov Mobility Pattern")
plt.xlabel("X (meters)")
plt.ylabel("Y (meters)")
plt.grid(True)
plt.legend()
plt.show()