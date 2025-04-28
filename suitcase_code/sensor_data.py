import time
import math

import RPi.GPIO as GPIO
from mpu6050 import mpu6050
import serial


def initialize_sensors():
 """
 Initialize configuration constants and set up sensors.
 Returns (door_pin, mpu_sensor, gps_serial).
 """
 # Configuration constants
 door_pin = 18
 mpu_addr = 0x68
 i2c_bus = 1
 gps_port = '/dev/serial0'
 gps_baud = 9600
 gps_timeout = 1 # seconds

 GPIO.setmode(GPIO.BCM)
 GPIO.setup(door_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

 mpu = mpu6050(mpu_addr, bus=i2c_bus)

 gps_serial = serial.Serial(gps_port, gps_baud, timeout=gps_timeout)

 return door_pin, mpu, gps_serial


def read_reed_switch(door_pin):
 return GPIO.input(door_pin) == GPIO.LOW


def detect_push(mpu, threshold=3.0, sample_delay=0.1):
 prev = mpu.get_accel_data(g=True)
 while True:
     current = mpu.get_accel_data(g=True)
     dx = current['x'] - prev['x']
     dy = current['y'] - prev['y']
     dz = current['z'] - prev['z']
     delta = math.sqrt(dx*dx + dy*dy + dz*dz)
     if delta > threshold:
         return True
     prev = current
     time.sleep(sample_delay)


def read_gps(gps_serial):
 def parse_degrees(raw, direction):
     val = float(raw)
     deg = int(val // 100)
     minutes = val - deg * 100
     dec = deg + minutes / 60
     if direction in ('S', 'W'):
         dec = -dec
     return dec

 while True:
     line = gps_serial.readline().decode('ascii', errors='ignore').strip()
     if line.startswith('$GPGGA'):
         parts = line.split(',')
         if len(parts) > 6 and parts[6] != '0' and parts[2] and parts[4]:
             lat = parse_degrees(parts[2], parts[3])
             lon = parse_degrees(parts[4], parts[5])
             return lat, lon
     time.sleep(0.1)
