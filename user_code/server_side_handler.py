import sys
import os
import requests as requests
import json as json

websitehost = "http://127.0.0.1:3000"


class ImageHandler:
    
    def __init__(self, webhost="http://127.0.0.1:3000"):

        self.__image_cache = dict()
        self.__webhost = webhost
    
    def request_more_images(self):

        filelist = self.__get_from_webhost("/images").json()

        for fname in filelist:
            if fname not in self.__image_cache:
                self.__image_cache[fname] = None

    def get_image_data(self, imgname):

        if self.__image_cache[imgname] == None:
            img_content = self.__get_from_webhost("/images/"+imgname).content
            self.__image_cache[imgname] = img_content
            print (img_content)
        return self.__image_cache[imgname]
    
    def get_all_imgnames(self):
        return self.__image_cache.keys()


    def __get_from_webhost(self, localpath):
        return requests.get(websitehost+localpath)
