# **Probabilistic 5G Handover & Traffic Congestion Simulation**

A system-level ECE project simulating a 5G Small-Cell Cluster. This repository models the interaction between realistic user mobility, stochastic wireless channel physics, and handover decision logic.

## **🚀 Overview**

In modern 5G networks, the "Ping-Pong Effect"—where a device rapidly switches between towers—is a major source of latency and battery drain. This project builds a simulation environment to test **Hysteresis-based Handover Logic** against realistic **Log-Normal Shadowing** and **Gauss-Markov Mobility**.

### **Key Features**

* **Phase 1 (Mobility):** Advanced Gauss-Markov model ensuring smooth, temporally-correlated user trajectories.  
* **Phase 2 (Physics):** Log-Normal Shadowing model incorporating Path Loss ($n=3.5$) and Gaussian noise ($\\sigma=6.0$ dB).  
* **Phase 3 (Logic):** Handover Controller with 3dB Hysteresis and Time-to-Trigger (TTT) logic to mitigate noise.

## **📊 Performance Analysis**

| Metric | Result | Engineering Significance |
| :---- | :---- | :---- |
| **Total Handovers** | \~968 | Reduced from \>13,000 (0dB Hys) to \~900 (3dB Hys), eliminating Ping-Ponging. |
| **Avg. Dropped Users** | 4.97% | Realistic modeling of "Dead Zones" below \-110 dBm sensitivity. |
| **Congestion Control** | Active | Managed tower capacity limit of 40 users/cell using load-balancing logic. |

## **🛠️ Installation & Usage**

1. **Clone the repository:**  
   git clone https://github.com/yourusername/5G-Handover-Sim.git

   pip install numpy matplotlib

3. **Run the Pipeline:**  
   * python mobility\_engine\_v2.py: Generates user paths.  
   * python physics\_engine.py: Calculates RSSI signal strengths.  
   * python network\_controller.py: Executes handover logic and generates load graphs.  
   * python final\_comparative\_study.py: Generates the Hysteresis impact bar chart.

## **📈 Results Visualization**

The simulation generates several plots:

* **Mobility Plot:** Shows smooth user trajectories across the 1km grid.  
* **RSSI Profile:** Visualizes the "noisy" signal jaggies caused by shadowing.  
* **Load Balancing:** Monitors real-time user count per tower vs. capacity limits.  
* **Comparative Study:** Proves the necessity of Hysteresis in reducing network overhead.

## 📄 License

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

