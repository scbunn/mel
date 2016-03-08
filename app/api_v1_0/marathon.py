"""Marathon Event API
This implements a simple REST(ish) API to support the marathon event bus.
https://mesosphere.github.io/marathon/docs/event-bus.html

"""
from flask import jsonify, request, abort, current_app
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
        current_app.logger.debug("bad format: {}".format(request.json))
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
    found = False
    for elem in eb['marathon_events']:
        if event_type in elem['eventType']:
            elements.append(elem)

    if elements:
        found = True

    return jsonify({'status': 'OK',
                    'found': found,
                    'events': elements})
