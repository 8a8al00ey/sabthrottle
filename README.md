# sabthrottle


## Description
Code taken from daghaian/nzbthrottle and changed to work with Sabnzbd.

Sabthrottle was designed in order to dynamically control the bandwidth allocation when users are actively streaming from Plex to avoid unnecessary buffering while still allowing the user to download at the fastest rate possible.

## Installation

*Note: Must have Python 3.5 or higher*

1. Run ```pip install -r requirements.txt``` from within the project root
2. Copy ```config_example.json``` and name the new file ```config.json```
3. Edit the config with all of your appropriate credentials

***Sample Config:***

```json
{
  "plex":
  {
    "url":"http://localhost:32400",
    "interval":60,
    "token": "daf32j3ik3l2k"
  },
  "sabnzbd":
  {
    "apikey":"123124sfdadsf",
    "url":"http://localhost:6789",
    "speeds":{
      "1":"50M",
      "2":"40M",
      "3":"30M",
      "4":"20M",
      "5":"10M"
    },
    "max_speed":"0M"
  },"notifications": {
    "Discord": {
      "enabled": false ,
      "url": "discord://webhook_id/webhook_token"
    },
    "Rocket.Chat": {
      "enabled": false,
      "url": "rocket://user:password@hostname/RoomID/Channel"
    },
    "Slack": {
      "enabled": false,
      "url": "slack://TokenA/TokenB/TokenC/Channel"
    },
    "Telegram": {
      "enabled": false,
      "url": "tgram://bottoken/ChatID"
    },
    "IFTTT": {
      "enabled": false,
      "url": "ifttt://webhooksID/EventToTrigger"
    },
    "PushBullet":{
      "enabled": false,
      "url": "pbul://accesstoken"
    },
    "Growl": {
      "enabled": false,
      "url": "growl://hostname"
    }
  }
}
```

***Plex***

```url``` - URL of your Plex Server

```interval``` - Interval with which to check for active streams (seconds)

```token``` - Your X-Plex-Token

***Sabnzbd***

```apikey``` - ApiKey for Sabnzbd

```url``` - URL of your Sabnzbd Client

```speeds``` - Define speed to throttle to based on number of active streams, ie 10000K or 10M

```max_speed``` - Define maximum speed when the throttle is lifted. Set to 0M if you wish to not use a limit or set this as same as your "Maximum line speed" in Config -> General -> Tunning (K|M)

***Notifications***

```enabled``` - Whether or not you wish to enable notifications via the selected service

```url``` - URL for the service you wish to enable (see https://github.com/caronc/apprise for formatting options of the URL)

## Usage

### Running script manually ###
```python throttle.py [-h] [--log-level=['DEBUG','INFO','WARN']]```

### Running script as service ###
If you do not wish to run the script manually, the module can be daemonized by copying the service file and running the script as a service. May need to modify location of script based on your preference by changing the following line in 'nzbthrottle.service' 
```
ExecStart=/usr/bin/python3 /opt/sabthrottle/throttle.py
```

### Running script in a Docker Container ###
```
docker run --name sabthrottle -d -v /PATH/TO/CONFIG.json:/sabthrottle/config.json 8a8al00ey/sabthrottle
```

## Support on Beerpay
Hey dude! Help me out for a couple of :beers:!

[![Beerpay](https://beerpay.io/daghaian/nzbthrottle/badge.svg?style=beer-square)](https://beerpay.io/daghaian/nzbthrottle)  [![Beerpay](https://beerpay.io/daghaian/nzbthrottle/make-wish.svg?style=flat-square)](https://beerpay.io/daghaian/nzbthrottle?focus=wish)