#sudo apt-get update
#sudo apt-get install python3-pip
#sudo apt-get install python3-dev
#sudo apt-get install i2c-tools
#pip3 install smbus2 spidev pyserial sqlite3

import serial
import sqlite3
import time

class fequency_grabber:
    __ser=None
    __conn=None
    __cursor=None
   
    def __init__(self):
        # Set the correct Serial port
        self.__ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        time.sleep(2)  # wait for Arduino to reset
        self.__ser.reset_input_buffer()

        # SQLite setup
        self.__conn = sqlite3.connect("qcm_data.db")
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS qcm_frequency (
                timestamp TEXT,
                frequency REAL
            )
        """)
        self.__conn.commit()

    def getQCMFreq(self):
        try:
            line = self.__ser.readline().decode('utf-8').strip()
            if line.isdigit():
                freq = float(line)
                print(f"Frequency: {freq} Hz")
                
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                self.__cursor.execute("INSERT INTO qcm_frequency (timestamp, frequency) VALUES (?, ?)",
                            (timestamp, freq))
                self.__conn.commit()
                return freq
            return -1
        except Exception as error:
            print(error)
            return -1
    
    def __del__(self):
        self.__ser.close()
        self.__conn.close()