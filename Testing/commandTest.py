USB_PORT = "/dev/ttyACM0"

import serial

def print_commands():
  print("Available commands:")
  print("   a - Retrieve Arduino value")
  print("   l - Turn on Arduino LED")
  print("   k - Turn off Arduino LED")
  print("   x - Exit Program")

try:
  usb = serial.Serial(USB_PORT, 9600, timeout=2)
except:
  print("ERROR - Could not open USB Serial Port. Please check port name and permissions")
  print("Exiting...")
  exit()

print("Enter a command from keyboard to send to Arduino")
print_commands()

while True:
  command = input("ENTER COMMAND: ")

  if command == "a":
    usb.write(b'read_a0')
    line = usb.readline()
    line = line.decode()
    line = line.strip()
    if line.isdigit():
      value = int(line)
    else:
      print("Unknown value '" + line + "', setting to 0.")
      value = 0
    print("Arduino A0 value: ", value)
  elif command == "l":
    usb.write(b"led_on")
    print("Arduino LED turned on.")
  elif command == "k":
    usb.write(b"led_off")
    print("Arduino LED turned off.")
  elif command == "x":
    print("Exiting...")
    exit()
  else:
    print("Unknown command")
    print_commands()
  