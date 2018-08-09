
import requests
import json
import xml.etree.ElementTree as ET
import logging
import time
import sys

class PlexServer(object):
    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                cfg = json.load(w)
                self._url = cfg['plex']['url']
                self._token =  cfg['plex']['token']
                self._interval =  cfg['plex']['interval']
        except Exception as e:
            self._logger.exception("Problem encountered when creating PlexServer object")
            sys.exit(1)

    def get_active_streams(self):
        try:
            r = requests.get(self._url + "/status/sessions",headers={'X-Plex-Token':self._token})
            if(r.status_code == 200):
                root = ET.fromstring(r.text)
                return root.attrib['size']
        except Exception as e:
            self._logger.exception("Failed to successfully request current active sessions")

    def monitor_active_streams(self):
        while(1):
            self._logger.info("Requesting active stream count...")
            active_streams = self.get_active_streams()
            if(active_streams != None):
                self._logger.info("Current stream count: %d",int(active_streams))
            self._logger.info("Sleeping for %d seconds before checking again",self._interval)
            time.sleep(self._interval)



