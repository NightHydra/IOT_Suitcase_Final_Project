import paho.mqtt.client as mqtt
import time
from final_project_image_handler import CameraHandler
import threading

CLIENT_ID = ""
THE_BROKER = "192.168.199.2"
BROKER_PORT = 1883

class MQTTHandler:
    def __init__(self):
        self.client = mqtt.Client(client_id=CLIENT_ID, clean_session=True)
        self.client.on_connect = self.__on_connect
        self.img_handler = CameraHandler()
        self.msg_num = 0

    def connect_to_broker(self):

        self.client.connect(THE_BROKER, port=BROKER_PORT, keepalive=60)
        self.client.loop_start()

    def start_publishing_loop(self):
        while True:
            img = self.img_handler.take_picture()
            self.client.publish("IOT_SUITCASE_DATA/IMAGES", qos=1, payload=img)
            self.msg_num += 1
            print(f"Published image {self.msg_num}")
            time.sleep(10)  # wait 10 seconds

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected with result code", rc)

# Create and start everything
mqtt_handler = MQTTHandler()
mqtt_handler.connect_to_broker()

# Start the publishing loop in the main thread
mqtt_handler.start_publishing_loop()
