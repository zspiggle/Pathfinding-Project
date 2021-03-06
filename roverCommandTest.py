SER_PORT = "/dev/ttyS0"

import serial

f = "f"
r = "r"
l = "l"
s = "s"
x = "x"

def print_commands():
  print("Available commands:")
  print("   f - Drive Forward")
  print("   r - Turn Right")
  print("   l - Turn Left")
  print("   s - Stop")
  print("   x - Exit Program")

try:
  ser = serial.Serial(SER_PORT, 9600, timeout=2)
except:
  print("ERROR - Could not open USB Serial Port. Please check port name and permissions")
  print("Exiting...")
  exit()

print("Enter a command from keyboard to send to Arduino")
print_commands()

while True:
  command = input("ENTER COMMAND: ")

  if command == "f":
    ser.write(b"f")
    print("Attempting to drive")
  elif command == "r":
    ser.write(b"r")
    print("Attempting to turn right")
  elif command == "l":
    ser.write(b"l")
    print("Attempting to turn left")
  elif command == "s":
    ser.write(b"s")
    print("STOP!")
  elif command == "x":
    print("Exiting...")
    exit()
  else:
    print("Unknown command")
    print_commands()
  