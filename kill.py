SER_PORT = "/dev/ttyS0"

import serial


s = "s"

try:
  ser = serial.Serial(SER_PORT, 9600, timeout=2)
except:
  print("ERROR - Could not open USB Serial Port. Please check port name and permissions")
  print("Exiting...")
  exit()
ser.write(b"s")
