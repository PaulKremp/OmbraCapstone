import numpy as np
import cv2
import requests
from requests.auth import HTTPDigestAuth
from http.client import RemoteDisconnected
from xmlrpc.client import ProtocolError
# API's found here https://drive.google.com/file/d/1VM2Tb-q4PhmZuvLxSk5OwWInbFxUuTR-/view


class camControl:
    def __init__(self, url, username: str, password: str):
        self.url = url    #Establish server address
        self.username = username #Username for camera access
        self.password = password #Password for camera access

    def getVideoMode(self):
        """Shows current video in mode of camera

        Returns:
            return video in Mode
        """
        r = requests.get("https://%s/cgi-bin/configManager.cgi?action=getConfig&name=VideoInDayNight" % self.url)
        
        return r

    def chooseVideoMode(self, url):
        """Selects whether the camera operates in day night mode
        Args:
            Mode

        Returns:
            set camera to desired mode

        """
        dict = {
        "Mode": "Color" "BlackWhite"
        }
        r = requests.get("https://%s/cgi-bin/configManager.cgi?action=setConfig&Mode=" % self.url)
            requests.get(self.urlGenerator(cgi_path),)
            self.request('cgi-bin/configManager.cgi',  {"Mode" : "Color", "Brightness", "BlackWhite", "Photoresistor", "Gain"})

        return

    def urlGenerator(self, cgi_path: str):
        """generates URLL for request
        Args:
            cgi_path : path for desired request after server name
            params: parameters to pass.
        """
        return f"http://{self.url}/{cgi_path}"

    def request(self, cgi_path: str, params):
        """Sends network request 
        Args:
            cgi_path: path for desired request after sever name
            params: parameters to pass
        """
        try:

            r = requests.get(self.urlGenerator(cgi_path),params = params,
            auth = HTTPDigestAuth(self.username, self.password),
            )
        except ConnectionError or ProtocolError or RemoteDisconnected:
            pass
        return r