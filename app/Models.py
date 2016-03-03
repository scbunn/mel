from datetime import datetime
from random import randint
from .exceptions import InvalidEvent


class MarathonEvent(object):
    """Base MEL event handler class"""
    id = 0   # static counter to track ids

    def __init__(self):
        MarathonEvent.id += 1
        self.id = MarathonEvent.id
        self.event_type = None
        self.timestamp = None
        self.raw_event = None

    def export_data(self):
        """export this event as a dictionary"""
        pass

    def import_data(self, data):
        """import initialize this event with data"""
        try:
            self.event_type = data['eventType']
            self.timestamp = data['timestamp']
            self.raw_event = data
        except KeyError as e:
            raise InvalidEvent('Invalid event data ' + e.args[0])


class MarathonApiEvent(MarathonEvent):
    def __init__(self):
        super(MarathonApiEvent, self).__init__()
        self.client = None
        self.app_id = None
        self.env = None
        self.ports = None
        self.health_checks = None

    def export_data(self):
        """export data as a dictionary"""
        return {
            'id': self.id,
            'event_type': self.event_type,
            'timestamp': self.timestamp,
            'client': self.client,
            'app_id': self.app_id,
            'env': self.env,
            'ports': self.ports,
            'health_checks': self.health_checks,
            'raw_event': self.raw_event,
        }

    def import_data(self, data):
        """initialize this event by importing data"""
        super(MarathonApiEvent, self).import_data(data)
        try:
            self.client = data['clientIp']
            self.app_id = data['appDefinition']['id']
            self.env = data['appDefinition']['env']
            self.ports = data['appDefinition']['ports']
            self.health_checks = data['appDefinition']['healthChecks']
        except KeyError as e:
            raise InvalidEvent('Invalid event data ' + e.args[0])

    @staticmethod
    def generate_fake_event():
        """Generate a fake API event"""
        ts = datetime.utcnow()
        client = "{}.{}.{}.{}".format(
            randint(1, 254), randint(1, 254),
            randint(1, 254), randint(1, 254)
        )
        app_id = "/my-app{}".format(randint(1, 1000))
        return {
            "eventType": "api_post_event",
            "timestamp": ts,
            "clientIp": client,
            "uri": "/v2/apps{}".format(app_id),
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
                "version": ts
            }
        }


if __name__ == "__main__":

    me1 = MarathonApiEvent()
    me2 = MarathonApiEvent()
    me1.import_data(MarathonApiEvent.generate_fake_event())
    me2.import_data(MarathonApiEvent.generate_fake_event())
    print(me1.export_data())
    print(me2.export_data())
