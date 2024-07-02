import serial
import os
import time

port = '/dev/volume-knob' if os.path.exists('/dev/volume-knob') else '/dev/ttyACM0'
baudrate = 115200

def initialize_serial_connection(port, baudrate):
  try:
    connection = serial.Serial(port, baudrate, timeout=1)
    return connection
  except (serial.SerialException, OSError) as e:
    print(f"Failed to connect to {port}: {e}")
    exit(1)

def read_line_from_serial(connection):
  try:
    line = connection.readline().strip().decode('utf-8')
    return line
  except serial.SerialException:
    print("SerialException: Device disconnected")
    connection.close()
    exit(0)
  except OSError as e:
    print(f"OSError: {e}")
    connection.close()
    exit(1)

def main():
  connection = initialize_serial_connection(port, baudrate)
  previous_volume = None

  while True:
    line = read_line_from_serial(connection)

    if not line:
      time.sleep(0.1)
      continue

    try:
      volume = int(line) * 2
      print(volume)

      if previous_volume is not None:
        if volume > previous_volume:
          volume -= 2
        elif volume < previous_volume:
          volume += 2

      if previous_volume != volume:
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ {volume}%')
        previous_volume = volume

    except ValueError:
      print("Error: Invalid integer received")
      continue

if __name__ == "__main__":
    main()
