"""Marathon Event API
This implements a simple REST(ish) API to support the marathon event bus.
https://mesosphere.github.io/marathon/docs/event-bus.html

"""
import requests
import sys
from psutil import virtual_memory
from flask import jsonify, request, abort, current_app, url_for
from . import api
from . import EVENT_BUFFERS as eb
from app.Models import MarathonApiEvent


@api.route('marathon/events/', methods=['GET'])
def get_events():
    """Return all events currently in the buffer"""
    response = []
    for event in eb['marathon_events']:
        response.append(event.export_data())

    return jsonify({'events': response})


@api.route('marathon/events/', methods=['POST'])
def create_event():
    """Accept incoming events and store then in a buffer to be processed"""
    if not request.json:
        current_app.logger.debug("Invalid request: {}".format(request))
        abort(400)
    e = MarathonApiEvent()
    e.import_data(request.json)
    eb['marathon_events'].append(e)
    return jsonify({'status': 'OK'}), 201


@api.route('marathon/events/<event_type>')
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
    else:
        return jsonify({'status': 'no elements found',
                        'search term': event_type}), 404


@api.route('marathon/events/testevent', methods=['POST'])
def generate_and_post_test_event():
    """Generate a test event and post it to our self"""
    current_app.logger.debug("posting to {}".format(
        url_for('api.create_event', _external=True)))
    r = requests.post(
        url_for('api.create_event', _external=True),
        json=MarathonApiEvent.generate_fake_event()
    )
    return jsonify({'status': '{}'.format(r.status_code)}), r.status_code


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
