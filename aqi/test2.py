import serial
import time
import matplotlib.pyplot as plt
import pandas as pd
from collections import deque

# 🔌 CONFIG
PORT = 'COM6'
BAUD = 9600

# 🔗 CONNECT
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)
    print(f"✅ Connected to {PORT}\n")
except:
    print("❌ Connection failed")
    exit()

# 📊 DATA STORAGE
data = []
window = deque(maxlen=5)  # for prediction

plt.ion()

# 🧠 AQI FUNCTION
def get_aqi_status(value):
    if value < 300:
        return "🟢 Good"
    elif value < 600:
        return "🟡 Moderate"
    else:
        return "🔴 Poor"

print("📡 Live Monitoring Started...\n")

while True:
    line = ser.readline().decode().strip()

    if line:
        try:
            value = int(line)

            # store data
            data.append(value)
            window.append(value)

            # 📊 Prediction (moving average)
            if len(window) == 5:
                prediction = sum(window) / len(window)
            else:
                prediction = value

            # 🧠 AQI
            status = get_aqi_status(value)

            # 🚨 Alert
            if value > 600:
                alert = "🚨 ALERT!"
            else:
                alert = ""

            print(f"Value: {value} | Predicted: {round(prediction,2)} | {status} {alert}")

            # 💾 Save data
            with open("air_log.csv", "a") as f:
                f.write(f"{time.time()},{value},{prediction}\n")

            # 📈 Plot
            plt.clf()

            # raw data
            plt.plot(data, label="Raw")

            # smoothed
            smooth = pd.Series(data).rolling(3).mean()
            plt.plot(smooth, label="Smoothed")

            # predicted line
            plt.axhline(y=prediction, linestyle='--', label="Prediction")

            plt.title("🔥 Live Air Quality System")
            plt.xlabel("Time")
            plt.ylabel("Sensor Value")
            plt.legend()
            plt.pause(0.1)

        except:
            pass