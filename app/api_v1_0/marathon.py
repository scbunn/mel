"""Marathon Event API
This implements a simple REST(ish) API to support the marathon event bus.
https://mesosphere.github.io/marathon/docs/event-bus.html

"""

import requests
import sys
from psutil import virtual_memory
from flask import jsonify, request, abort, current_app, url_for
from app.Models import MarathonApiEvent
from . import api
from . import EVENT_BUFFERS as eb
from .errors import ValidationError


@api.route('events/', methods=['GET'])
def get_events():
    """Return all events currently in the buffer"""
    response = []
    for event in eb['marathon_events']:
        response.append(event.export_data())

    return jsonify({'events': response})


@api.route('events/', methods=['POST'])
def create_event():
    """Accept incoming events and store then in a buffer to be processed"""
    if not request.json:
        current_app.logger.debug("Invalid request: {}".format(request))
        raise ValidationError("Invalid request format!")
    e = MarathonApiEvent()
    e.import_data(request.json)
    eb['marathon_events'].append(e)
    return jsonify({}), 201, {'Location': e.get_url()}


@api.route('events/<int:event_id>')
def get_event_by_id(event_id):
    """Return an event based on event id"""
    for event in eb['marathon_events']:
        if event.id == event_id:
            return jsonify({'event': event.export_data()})
    abort(404)


@api.route('events/<event_type>')
def get_event(event_type):
    """Return all events of event_type"""
    current_app.logger.debug("search for event type: {}".format(event_type))
    elements = []
    for elem in eb['marathon_events']:
        if event_type in elem.event_type:
            elements.append(elem.export_data())

    if elements:
        return jsonify({"count": len(elements),
                        event_type: elements})
    abort(404)


@api.route('events/testevent', methods=['POST'])
def generate_and_post_test_event():
    """Generate a test event and post it to our self"""
    current_app.logger.debug("posting to {}".format(
        url_for('api.create_event', _external=True)))
    r = requests.post(
        url_for('api.create_event', _external=True),
        json=MarathonApiEvent.generate_fake_event()
    )
    rv = {
        'status': r.status_code,
        'message': 'event generated',
        'location': r.headers['location']
    }
    return jsonify(rv), r.status_code


@api.route('health', methods=['GET'])
def health_check():
    """return a health status of the framework"""
    b = eb['marathon_events']
    mem = virtual_memory()
    bsize = 0
    for e in b:
        bsize += sys.getsizeof(e)

    response = {
        'buffers': {
            'buffer size': b.maxlen,
            'events buffered': b.get_size(),
            'memory size': bsize + sys.getsizeof(b)
        },
        'memory': {
            'total': mem.total / 1048576,
            'available': mem.available / 1048576,
            'percent': mem.percent,
            'used': mem.used / 1048576,
            'free': mem.free / 1048576
        }
    }

    return jsonify(response)
