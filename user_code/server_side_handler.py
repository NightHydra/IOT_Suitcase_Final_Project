# server_side_handler.py
import sys
import os
import requests
import ssl
import json as json

# Print OpenSSL version for debugging
print(ssl.OPENSSL_VERSION)

#cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1,
#                                       open('cert/IOT_Suitcase.crt').read())

websitehost = "https://localhost:3000"

class DataHandler:

    
    
    def __init__(self, webhost=websitehost):

        self.__image_cache = dict()
        self.__new_images = []

        self.__webhost = webhost
        self.__sess = requests.Session()
        # If you have a certificate, set verify path
        #self.__sess.verify = "cert/cert.pem"

    def login_to_server(self, uname : str, pwd : str):

        response = self.__sess.post(f"{websitehost}/login", data={
            'username': uname,
            'password': pwd
            }, verify=False)
    
        if response.status_code == 401:
            return False
        return True

    
    def request_more_images(self):
        resp = self.__sess.get(f"{self.__webhost}/images", verify=False)
        resp.raise_for_status()

        self.__new_images = []
        for fname in resp.json():
            if fname not in self.__image_cache:
                self.__image_cache[fname] = None
                self.__new_images.append(fname)

    
    def get_all_imgnames(self):
        return list(self.__image_cache.keys())
    
    def get_new_imagenames(self):
        return self.__new_images

    def get_image_data(self, imgname: str) -> bytes:
        if self.__image_cache.get(imgname) is None:
            resp = self.__sess.post(
                f"{self.__webhost}/images",
                data={'filename': imgname},
                verify=False
            )
            resp.raise_for_status()
            self.__image_cache[imgname] = resp.content
        return self.__image_cache[imgname]
    
    def get_event_data(self):

        resp = self.__sess.get(self.__webhost+"/events", verify=False)

        if (resp.content.decode() == "NA"):
            return {}
        else:
            decoded_msg = resp.content.decode().split("\n")
            
            while "" in decoded_msg:
                decoded_msg.remove("")

            return list(map(json.loads, decoded_msg))

