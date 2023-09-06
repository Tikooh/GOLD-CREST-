import numpy as np
from filterpy.kalman import KalmanFilter

# Initialize data structures
timestamps = []  # List to store timestamps
measurements = []  # List to store sensor measurements
estimated_positions = []  # List to store estimated positions

# Create a Kalman filter for 2D position tracking (x, y)
kf = KalmanFilter(dim_x=4, dim_z=2)

# Initialize the state estimate and covariance matrix
kf.x = np.array([0, 0, 0, 0])
kf.P *= 1e3

# Define a function to update the Kalman filter with new data
def update_kalman_filter(new_timestamp, new_measurement):
    # Calculate the time interval (Δt) since the last measurement
    if timestamps:
        delta_t = new_timestamp - timestamps[-1]
    else:
        delta_t = 0.0
    
    # Update the state transition matrix and scale the process noise covariance
    kf.F = np.array([[1, 0, delta_t, 0],
                     [0, 1, 0, delta_t],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])
    kf.Q *= delta_t  # Scale the process noise covariance
    
    # Update the Kalman filter with the new measurement
    kf.update(new_measurement)
    
    # Store the new timestamp, measurement, and estimated position
    timestamps.append(new_timestamp)
    measurements.append(new_measurement)
    estimated_positions.append(kf.x[:2])

# Main loop for updating the Kalman filter
while True:
    # Simulate data arrival (replace with actual data)
    new_timestamp = time.time()  # Replace with actual timestamp
    new_measurement = np.array([drone_x, drone_y])  # Replace with actual measurements
    
    # Update the Kalman filter with the new data
    update_kalman_filter(new_timestamp, new_measurement)
    
    # Use the estimated position for control or further processing
    # For example, you can print the estimated position:
    print(f"Estimated Position: {kf.x[:2]}")
