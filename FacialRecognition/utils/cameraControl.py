import numpy as np
import cv2
import requests
# API's found here https://drive.google.com/file/d/1VM2Tb-q4PhmZuvLxSk5OwWInbFxUuTR-/view


class camControl:
    def __init__(self, server,mode):
        self.server = server    #Establish server address
        self.mode = mode #Day/Night or IR Mode of Camera

    def getLightSettings(self,server):
        """Shows current light settings of camera

        Returns:
            return list of camera light settings
        """
        r = requests.get("https://%s/cgi-bin/configManager.cgi?action=getConfig&name=Lighting" % server)
        
        return r

    def chooseLightMode(self, server,mode):
        """Selects whether the camera operates in day night mode
        Args:
            Mode

        Returns:
            set camera to desired mode

        """
        r = requests.get("https://%s/cgi-bin/configManager.cgi?action=setConfig&Mode=%s" % server,mode)


        return