#sudo apt-get update
#sudo apt-get install python3-pip
#sudo apt-get install python3-dev
#sudo apt-get install i2c-tools
#pip3 install smbus2 spidev pyserial sqlite3

import serial
import sqlite3
import time

# Set the correct Serial port
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)  # wait for Arduino to reset

# SQLite setup
conn = sqlite3.connect("qcm_data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS qcm_frequency (
        timestamp TEXT,
        frequency REAL
    )
""")
conn.commit()

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line.isdigit():
            freq = float(line)
            print(f"Frequency: {freq} Hz")
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("INSERT INTO qcm_frequency (timestamp, frequency) VALUES (?, ?)",
                           (timestamp, freq))
            conn.commit()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
    conn.close()