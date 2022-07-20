import plex
import sab
import notification
import json
import time
import argparse
import logging.handlers
from helpers import stream_throttle_helpers as stream_helper


def start_monitor():
    try:
        lastThrottleState = False
        last_active_streams = 0
        #Initially set speed of sabnzbd to unthrottle or the user defined maxSpeed
        sabServer.set_start_speed()
        while (1):
            logger.info("Requesting plex active stream count...")
            active_streams = plexServer.get_active_streams()
            logger.debug("active_streams is %s", active_streams)
            state = sabServer.get_current_throttle_status()
            logger.debug("State = %s ", state)
            logger.debug("lastThrottleState = %s", lastThrottleState)
            if(state == False and lastThrottleState == True):
                    logger.debug("Previous state of throttle flag was True but currently throttled, changing to False!")
                    lastThrottleState = False
            elif(state == True and lastThrottleState == False):
                    logger.debug("Previous state of throttle flag was False but currently not throttled, changing to True!")
                    last_active_streams = plexServer.get_active_streams()
                    lastThrottleState = True
            
            logger.debug("Last stream count {} and active stream count {}".format(last_active_streams,plexServer.get_active_streams()))
            if (last_active_streams == plexServer.get_active_streams()):
                logger.info("Plex stream count of %s, has not changed will not change throttle", active_streams)
            elif (active_streams != None):
                logger.info("Current plex stream count: %s", active_streams)
                if (lastThrottleState):
                    if (active_streams == 0):
                        logger.info("Streams are 0 and we are currently throttled. Lifting the limit")
                        throttleResponse = sabServer.throttle_streams(active_streams)
                        if(throttleResponse != -1):
                            lastThrottleState = False
                            last_active_streams = active_streams
                            logger.info("Throttle lifted successfully")
                            try:
                                notifyClient.notify("Streams are 0 and we were throttled. Lifted the limit")
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                    elif(active_streams != last_active_streams):
                        logger.info("Already throttled, but stream count has changed, adjusting speed")
                        throttleResponse = sabServer.throttle_streams(active_streams)
                        if (throttleResponse != -1):
                            last_active_streams = active_streams
                            logger.info("Speed throttling adjusted successfully")
                            try:
                                notifyClient.notify("Stream count has changed to {}, adjusted speed to: {}B/s".format(active_streams,throttleResponse))
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                    else:
                        logger.info("Already throttled with no change. Continuing to monitor.")
                else:
                    if (active_streams > 0):
                        logger.info("There are currently active streams. Proceeding to throttle SAB")
                        throttleResponse = sabServer.throttle_streams(active_streams)
                        logger.debug("throttleResponse is %s",throttleResponse)
                        if (throttleResponse != -1):
                            logger.info("SAB throttled successfully, throttled to: {}B/s".format(throttleResponse))
                            lastThrottleState = True
                            last_active_streams = active_streams
                            try:
                                notifyClient.notify("Currently {} active streams, throttled to: {}B/s".format(active_streams,throttleResponse))
                            except Exception as e:
                                logger.error("Error encountered when attempting to send notification")
                        else:
                            logger.error("Something went wrong when attempting to throttle SAB")
                    else:
                        logger.info("No active streams ensuring correct unthrottle speed is set")
                        throttleResponse = sabServer.throttle_streams(0)
                        if(throttleResponse != -1):
                            logger.info("Unthrottled speed set correctly to: {}B/s".format(throttleResponse))
                            last_active_streams = active_streams
            logger.info("Sleeping for %d seconds before checking again", plexServer.get_interval())
            time.sleep(plexServer.get_interval())
    except Exception as e:
        logger.exception("Start monitor encountered exception. Trying again in 60 seconds")

        time.sleep(60)

#=======================================================#
#                       INIT                            #
#=======================================================#

#Grab command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--log-level',type=str,default='INFO',choices=['INFO','DEBUG','WARN'],help="Level of Logging Desired (Default: INFO)")

#Initialize Logging
logger = logging.getLogger()
logger.setLevel(parser.parse_args().log_level)

# create a file handler
# Max Log Size - 10 MB
# Max Log Count - 1
fh = logging.handlers.RotatingFileHandler('./sabthrottle.log',maxBytes=10 * 1024 * 1024 , backupCount=1)

# create console handler
ch = logging.StreamHandler()

# create a logging format
formatter = logging.Formatter('%(asctime)s-%(module)-6s: %(levelname)-8s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S ')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# initialize notification client
notifyClient = notification.NotificationClient()
# initialize plex server
plexServer = plex.PlexServer()
# initialize Sab server
sabServer = sab.SAB()

while(1):
    start_monitor()
