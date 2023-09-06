import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima_model import ARIMA

# Initialize data structures
timestamps = []  # List to store timestamps
coordinates = []  # List to store drone coordinates

# Define the maximum number of data points to keep in the time series
max_data_points = 100  # Adjust as needed

# Create a function to update the time series
def update_time_series(new_timestamp, new_coordinate):
    timestamps.append(new_timestamp)
    coordinates.append(new_coordinate)
    
    # Ensure we only keep the last `max_data_points` data points
    if len(timestamps) > max_data_points:
        timestamps.pop(0)
        coordinates.pop(0)

# Create a function to predict the future position
def predict_future_position():
    if len(coordinates) < 2:
        # Not enough data to make a prediction
        return None

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame({'timestamp': timestamps, 'coordinate': coordinates})
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Convert timestamps to datetime objects

    # Set the timestamp as the index
    df.set_index('timestamp', inplace=True)

    # Resample data to a fixed time interval (e.g., 1 second) to ensure regular time intervals
    df_resampled = df.resample('1S').mean()
    
    # Check for missing values and fill them if necessary
    df_resampled['coordinate'].fillna(method='ffill', inplace=True)

    # Fit an ARIMA model to the resampled data
    model = ARIMA(df_resampled['coordinate'], order=(1, 1, 0))  # Adjust order as needed
    model_fit = model.fit(disp=0)

    # Predict the future position (1 second into the future)
    future_position = model_fit.forecast(steps=1)[0]

    return future_position

# Simulate real-time data arrival (replace this with your data source)
import time

while True:
    # Simulate data arrival
    new_timestamp = time.time()  # Replace with the actual timestamp
    new_coordinate = np.random.rand()  # Replace with actual drone coordinate
    update_time_series(new_timestamp, new_coordinate)
    
    # Predict the future position
    future_position = predict_future_position()
    
    if future_position is not None:
        print(f"Predicted Future Position: {future_position}")
    
    # Adjust the loop rate as needed to match your data arrival rate
    time.sleep(1)  # Sleep for 1 second before the next iteration
