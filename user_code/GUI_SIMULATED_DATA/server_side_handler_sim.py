import sys
import os
import requests
import json
import ssl
import time
import random

# Print OpenSSL version
print(ssl.OPENSSL_VERSION)

# Server host configuration
websitehost = "https://129.161.50.234:3000"

class DataHandler:
    """
    Handles image fetching and caching from the server.
    """
    def __init__(self, webhost=websitehost):
        self.__image_cache = dict()
        self.__webhost = webhost
        self.__sess = requests.Session()
        self.__sess.verify = "cert/cert.pem"

    def login_to_server(self, uname: str, pwd: str):
        self.__sess.post(
            f"{websitehost}/login",
            data={'username': uname, 'password': pwd},
            verify=False
        )

    def request_more_images(self):
        filelist = self.__get_from_webhost("/images").json()
        for fname in filelist:
            if fname not in self.__image_cache:
                self.__image_cache[fname] = None

    def get_image_data(self, imgname):
        if self.__image_cache.get(imgname) is None:
            resp = self.__sess.post(
                websitehost + "/images",
                data={"filename": imgname},
                verify=False
            )
            self.__image_cache[imgname] = resp.content
        return self.__image_cache[imgname]

    def get_all_imgnames(self):
        return list(self.__image_cache.keys())

    def __get_from_webhost(self, localpath):
        return self.__sess.get(self.__webhost + localpath, verify=False)


# --- Sensor Simulation ---

def initialize_sensors():
    """
    Stub initializer, no real hardware.
    """
    print("initialize_sensors() called (stub)")
    return None, None, None


def read_reed_switch(door_pin=None):
    """
    Simulate reed switch toggling state each call.
    """
    state = random.choice([True, False])
    print(f"Simulated reed switch: {'OPEN' if state else 'CLOSED'}")
    return state


def detect_push(mpu=None, threshold=3.0, sample_delay=0.1):
    """
    Randomly simulate a push ~30% of the time.
    """
    if random.random() < 0.3:
        mag = round(random.uniform(threshold, threshold + 2.0), 2)
        print(f"Simulated PUSH detected! Magnitude: {mag}")
        return mag
    return 0


def read_gps(gps_serial=None):
    """
    Return fixed GPS coordinates (stub).
    """
    lat, lon = 40.7128, -74.0060
    print(f"Simulated GPS: {lat}, {lon}")
    return lat, lon

class SensorHandler:
    """
    Wrapper for stub sensor functions, returning timestamped events.
    """
    def __init__(self):
        self.door_pin, self.mpu, self.gps_serial = initialize_sensors()
        self.last_switch_state = read_reed_switch(self.door_pin)

    def get_recent_events(self):
        events = []

        # 1) Reed switch change
        current = read_reed_switch(self.door_pin)
        if current != self.last_switch_state:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            state_str = "OPEN" if current else "CLOSED"
            events.append({
                "type": "SWITCH",
                "state": state_str,
                "timestamp": ts
            })
            self.last_switch_state = current

        # 2) Push detection
        mag = detect_push(self.mpu)
        if mag:
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            events.append({
                "type": "PUSH",
                "magnitude": mag,
                "timestamp": ts
            })

        # 3) GPS reading
        lat, lon = read_gps(self.gps_serial)
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        events.append({
                "type": "GPS",
                "lat": lat,
                "lon": lon,
                "timestamp": ts
        })

        return events
