
import paho.mqtt.client as mqtt
import time as time
from final_project_image_handler import CameraHandler

CLIENT_ID = ""
THE_BROKER = "192.168.199.1"
BROKER_PORT = 8884

class MQTTHandler:
	def __init__(self):
		self.client = mqtt.Client(client_id=CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
		self.client.on_publish = self.__on_publish
		self.client.on_connect = self.__on_connect
		
		self.img_handler = CameraHandler()
		
		self.msg_num = 0
		
	def publish_image_to_server(self, msg):
		self.client.publish("IOT_SUITCASE_DATA/IMAGES", qos=1, retain=False, payload = msg)
		
		
	def connect_to_broker(self):
		self.client.connect(THE_BROKER, port=BROKER_PORT, keepalive=60)
		
	def start_client(self):
		
		self.publish_image_to_server("Hello World")
		
		self.client.loop_forever()
	
	def __on_connect(self, client, userdata, flags, rc):
		
		print ("CONNECTED!!")
		
	def __on_publish(self, client, userdata, mid):
		self.msg_num += 1
		time.sleep(10)
		self.publish_image_to_server(self.img_handler.take_picture())


mqtt_handler = MQTTHandler()

mqtt_handler.connect_to_broker()

mqtt_handler.start_client()
		
