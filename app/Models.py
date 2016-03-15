from datetime import datetime
from random import randint
from flask import url_for
from .exceptions import InvalidEvent


class MarathonEventBase(object):
    """Base MEL event handler class"""
    id = 0   # static counter to track ids

    def __init__(self):
        MarathonEventBase.id += 1
        self.id = MarathonEventBase.id

    def get_url(self):
        """return a url to retrieve this event from"""
        return url_for('api.get_event_by_id', event_id=self.id, _external=True)

    @staticmethod
    def generate_fake_event():
        """Generate a random fake event"""
        ts = datetime.utcnow().isoformat()
        client = "{}.{}.{}.{}".format(
            randint(1, 254), randint(1, 254),
            randint(1, 254), randint(1, 254)
        )
        events = [
            'api_event'
        ]
        event_callbacks = {
            'api_event': MarathonEventBase.create_fake_apiEvent(ts, client),
        }
        rand_event = randint(0, len(events))
        return event_callbacks[events[rand_event - 1]]

    @staticmethod
    def create_fake_apiEvent(timestamp, clientIp):
        """Generate a fake API event"""
        app_id = "/testapp/{}".format(randint(1, 1000))
        return {
            "eventType": "api_post_event",
            "timestamp": timestamp,
            "clientIp": clientIp,
            "uri": "/v2/apps/testapp/{}".format(app_id),
            "appDefinition": {
                "args": [],
                "backoffFactor": 1.15,
                "backoffSeconds": 1,
                "cmd": "sleep {}".format(randint(1, 60)),
                "constraints": [],
                "container": "",
                "cpus": 0.2,
                "dependencies": [],
                "disk": 0.0,
                "env": {'DEBUG': True},
                "executor": "",
                "healthChecks": [],
                "id": "{}".format(app_id),
                "instances": 2,
                "mem": 32.0,
                "ports": [randint(1, 64000), randint(1, 64000)],
                "requirePorts": False,
                "storeUrls": [],
                "upgradeStrategy": {
                    "minimumHealthCapacity": 1.0
                },
                "uris": [],
                "user": "",
                "version": randint(1, 255)
            }
        }


class MarathonEvent(MarathonEventBase):
    def __init__(self):
        super(MarathonEvent, self).__init__()
        self.eventType = None
        self.timestamp = None
        self.marathon_host = None
        self.event = None

    def export_data(self):
        """return this event as a dictionary to the caller"""
        return {
            'id': self.id,
            'eventType': self.eventType,
            'timestamp': self.timestamp,
            'marathon_host': self.marathon_host,
            'url': self.get_url(),
            'event': self.event
        }

    def import_data(self, data):
        """Initialize this event by importing the passed data.
        data is expected to be a flask request object. Try and load all data
        from json and bail in missing data as invalid
        """
        if not data.json:
            raise InvalidEvent('request does not appear to be valid JSON')

        try:
            self.timestamp = data.json['timestamp']
            self.eventType = data.json['eventType']
            self.event = data.json
            self.marathon_host = data.remote_addr
        except KeyError as e:
            raise InvalidEvent('Invalid event data ' + e.args[0])


if __name__ == "__main__":
    me1 = MarathonEvent()
    me2 = MarathonEvent()
    me1.import_data(MarathonEventBase.generate_fake_event())
    me2.import_data(MarathonEventBase.generate_fake_event())
    print(me1.export_data())
    print(me2.export_data())
