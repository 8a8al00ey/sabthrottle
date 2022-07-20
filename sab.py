import logging
import requests
from urllib.parse import urlparse
import json
import sys
from helpers import stream_throttle_helpers as stream_helper

class SAB(object):
    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                self._logger.debug("Loading SAB config.json")
                cfg = json.load(w)
                self._logger.debug("SAB Config loaded successfully" + str(cfg))
                self._url = cfg['sabnzbd']['url']
                self._apikey = cfg['sabnzbd']['apikey']
                self._speedIncrements = cfg['sabnzbd']['speeds']
                self._maxSpeed = cfg['sabnzbd']['max_speed']
        except Exception as e:
            self._logger.exception("Problem encountered when creating SAB object")
            sys.exit(1)
    def get_maxSpeed(self):
        return self._maxSpeed
    def set_start_speed(self):
        self._logger.info("Setting initial speed for SAB as %s",self._maxSpeed if self._maxSpeed else 0)
        self.throttle_streams(0)

    def get_speedIncrements(self):
        return self._speedIncrements

    def get_current_throttle_status(self):
        self._logger.debug("Grabbing current state of sabnzbd")
        currStatus = json.loads(self.run_method("queue"))
        self._logger.debug("currStatus is is %s", currStatus)
        if(currStatus != None):
            self._logger.debug("Current status of sabnzbd is %s",currStatus)
            self._logger.debug("Current rate of sabnzbd download is %s",currStatus['queue']['speedlimit_abs'])
            if(currStatus['queue']['speedlimit_abs'] == "" or (self._maxSpeed and currStatus['queue']['speedlimit_abs'] >= (self._maxSpeed * 1000))):

                self._logger.debug("SAB is current NOT throttled, returning False")
                return False
            else:
                self._logger.debug("SAB is currently throttled with a speed of %s. Returning true",currStatus['queue']['speedlimit_abs'])
                return True
        else:
            self._logger.error("Something went wrong when requesting the current status of sabnzbd")


    def throttle_streams(self,active_streams):
        currRate = 0 if not self._maxSpeed else self._maxSpeed
        self._logger.debug("Active_streams %s", active_streams)
        if(active_streams != 0):
            currRate = stream_helper.find_nearest(self._speedIncrements,active_streams)
        throttleResponse = json.loads(self.run_method("value",currRate))
        self._logger.debug("throttleResponse = %s", throttleResponse)
        self._logger.debug(type(throttleResponse))
        if ("status" in throttleResponse and throttleResponse['status'] == True):
            return currRate
        return -1


    def _form_request_url(self):
        try:
            url = urlparse(self._url)
            return "{scheme}://{netloc}/api?output=json&apikey={apikey}".format(scheme=url.scheme,apikey=requests.compat.quote_plus(self._apikey),netloc=url.netloc)
        except Exception as e:
            self._logger.exception("Error encountered when formatting provided url for sabnzbd requests")

    def run_method(self,method,params=None):
        try:
            if method == "value":
                self._logger.debug("Requesting method: " + str(method) + " with params: " + str(params))
                r = requests.get(self._form_request_url(),params={"mode":"config","name":"speedlimit",f"{method}": f"{str(params)}"})
            else:
                self._logger.debug("Requesting method: " + str(method) + " with params: " + str(params))
                r = requests.get(self._form_request_url(),params={"mode":method} )
    
            if(r.status_code == 200):
                self._logger.debug("Response from Sabnzbd: " + str(r.text))
                return r.text
            else:
                self._logger.error("Did not get expected response from SAB API: %s",r.text)
                return None
        except Exception as e:
            self._logger.exception("Error encountered when requesting method: " + str(method) + " with params: " + str(params))
