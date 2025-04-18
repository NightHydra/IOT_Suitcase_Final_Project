import base64

class CameraHandler:
	
	def __init__(self):
		
		pass
	
	def take_picture(self):
		
		with open("testpic.jpg", "rb") as imgfile:
			
			pic = base64.b64encode(imgfile.read())
			print ("Picture Sent to Client")
			return pic
