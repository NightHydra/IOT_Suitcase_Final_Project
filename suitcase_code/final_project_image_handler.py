from picamera2 import Picamera2
import io
import base64
from PIL import Image

class CameraHandler:
    def __init__(self):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_still_configuration())
        self.cam.start()

    def take_picture(self):
        # Capture image as PIL image
        image = self.cam.capture_image()

        # Convert image to bytes
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='JPEG')
        img_bytes.seek(0)

        # Base64 encode
        encoded = base64.b64encode(img_bytes.read()).decode('utf-8')
        print("Picture Sent to Client")
        return encoded
