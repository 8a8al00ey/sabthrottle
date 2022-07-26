import apprise
import json
import logging
import sys

class NotificationClient(object):
    def __init__(self):
        self._logger = logging.getLogger()
        try:
            with open("./config.json") as w:
                self._logger.debug("Loading Notification Data from config.json")
                cfg = json.load(w)
                self._logger.debug("Notification Data loaded successfully" + str(cfg))
                self._notifier = apprise.Apprise(asset=apprise.AppriseAsset(
                    image_url_mask="https://avatars.githubusercontent.com/u/960698?s=200&v=4",
                    default_extension=".jpeg"))
                for k,v in cfg['notifications'].items():
                    if(v['enabled'] == True):
                        self._notifier.add(v['url'])
        except Exception as e:
            self._logger.exception("Problem encountered when creating Notification object")
            sys.exit(1)

    def notify(self,message):
        self._notifier.notify(
            title='SABThrottle Notification',
            body=message
        )
