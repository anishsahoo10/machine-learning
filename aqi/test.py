import serial
import time
import matplotlib.pyplot as plt

PORT = 'COM6'
BAUD = 9600

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

plt.ion()  # interactive mode

data = []

print("📡 Live monitoring started...\n")

while True:
    line = ser.readline().decode().strip()

    if line:
        try:
            value = int(line)
            print("Value:", value)

            data.append(value)

            # keep last 50 values
            if len(data) > 50:
                data.pop(0)

            plt.clf()
            plt.plot(data)
            plt.title("Live Air Quality")
            plt.xlabel("Time")
            plt.ylabel("Sensor Value")
            plt.pause(0.1)

        except:
            pass