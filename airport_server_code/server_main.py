import base64
import paho.mqtt.client as mqtt
import datetime as dt

THE_BROKER = "192.168.88.88"
CLIENT_ID = ""
BROKERS_PORT = 1883

FSAVPATH = "full_internet_server_code/files_to_serve/images/"

class MQTTServer:
    
    def __init__(self):
        
        self.__topics_to_rx_from_and_functions_to_run_once_rxd = \
            {
                "IOT_SUITCASE_DATA/IMAGES": self.image_handler,
                "IOT_SUITCASE_DATA/LOCATION_DATA" : self.loc_data_handler
            }
        
        self.client = mqtt.Client(client_id=CLIENT_ID, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION1)

        self.client.on_connect = self.__on_connect
        self.client.on_publish = self.__on_publish
        self.client.on_message = self.__on_message

        self.client.username_pw_set(None, password=None)

        self.__ready_to_send_next_msg = False

    def __on_connect(self, client, userdata, flags, rc):

        # Once we connect, subscribe to all topics.  We are just using the broker
        #    so we can later process HTTP requests allowing users to pull data from
        #    the server
        for topic in self.__topics_to_rx_from_and_functions_to_run_once_rxd.keys():
            self.client.subscribe(topic, qos=1)
        print ("SERVER SUCCESSFULLY STARTED")
        
    
    def __on_publish(self, client, userdata, mid):
        # We really shouldnt need to publish anything so pass
        pass

    def __on_message(self, client, userdata, msg):
        # message = str(msg.payload.decode("utf-8"))
        print("Encoded image data received and saved as 'received_image.jpg'")
        self.__topics_to_rx_from_and_functions_to_run_once_rxd[msg.topic](msg.payload)

    def connect_to_server(self, provided_host, provided_port):

        self.client.connect(provided_host, provided_port)
        

    def image_handler(self, decoded_msg):
        with open(FSAVPATH+"received_image-" + dt.datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
        , "wb") as f:
            f.write(base64.b64decode(decoded_msg))
        print ("image Processed and saved")
    
    def loc_data_handler(self, decoded_msg):
        print ("Location Data Received", decoded_msg)
    
    def start_server(self):
        self.client.loop_forever()

server = MQTTServer()
server.connect_to_server(THE_BROKER, BROKERS_PORT)

server.start_server()

