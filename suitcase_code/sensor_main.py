import threading
import time
import RPi.GPIO as GPIO

from sensor_data import initialize_sensors, read_reed_switch, detect_push

def monitor_reed(door_pin, interval=0.5):
    while True:
        is_open = read_reed_switch(door_pin)
        state = "OPEN" if is_open else "CLOSED"
        print(f"Reed switch is {state}")
        time.sleep(interval)

def monitor_push(mpu, threshold=3.0):
    while True:
        print("Waiting for strong shove…")
        try:
            detect_push(mpu, threshold=threshold)
            print("⚠️  Push detected!")
        except Exception as e:
            print(f"Error reading MPU6050: {e}")
            return


def main():
    door_pin, mpu, gps_serial = initialize_sensors()

    try:
        accel = mpu.get_accel_data()
        print(f"MPU6050 detected successfully. First accel reading: {accel}")
    except Exception as e:
        print(f"Failed to read from MPU6050: {e}")
        GPIO.cleanup()
        return

    try:
        t_reed = threading.Thread(target=monitor_reed, args=(door_pin,), daemon=True)
        t_push = threading.Thread(target=monitor_push, args=(mpu,), daemon=True)
        t_reed.start()
        t_push.start()

        while True:
            time.sleep(1)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
