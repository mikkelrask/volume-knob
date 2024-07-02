#!/usr/bin/env python3
import serial
import os
import time
import logging

# Setup logging
logging.basicConfig(filename='/tmp/volume_control.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

port = '/dev/volume-knob' if os.path.exists('/dev/volume-knob') else '/dev/ttyACM0'
baudrate = 115200

def initialize_serial_connection(port, baudrate):
  try:
    connection = serial.Serial(port, baudrate, timeout=1)
    logging.debug(f"Connected to {port} at {baudrate} baud.")
    return connection
  except (serial.SerialException, OSError) as e:
    logging.error(f"Failed to connect to {port}: {e}")
    exit(1)

def read_line_from_serial(connection):
  try:
    line = connection.readline().strip().decode('utf-8')
    logging.debug(f"Read line: {line}")
    return line
  except serial.SerialException:
    logging.error("SerialException: Device disconnected")
    connection.close()
    exit(0)
  except OSError as e:
    logging.error(f"OSError: {e}")
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
      logging.debug(f"Volume: {volume}")

      if previous_volume is not None:
        if volume > previous_volume:
          volume -= 2
        elif volume < previous_volume:
          volume += 2

      if previous_volume != volume:
        os.system(f'pactl set-sink-volume @DEFAULT_SINK@ {volume}%')
        logging.debug(f"Set volume to {volume}%")
        previous_volume = volume

    except ValueError:
      logging.error("Error: Invalid integer received")
      continue

if __name__ == "__main__":
  logging.debug("Script started")
  main()
