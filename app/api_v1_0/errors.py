from flask import jsonify
from . import api
from ..exceptions import ValidationError, InvalidEvent


@api.errorhandler(405)
def method_not_supported(e):
    response = jsonify({'status': 405, 'error': 'method not supported',
                       'message': 'the method called is not supported'})
    response.status_code = 405
    return response


@api.errorhandler(InvalidEvent)
@api.errorhandler(ValidationError)
def bad_request(e):
    response = jsonify({'status': 400, 'error': 'bad request',
                        'message': e.args[0]})
    response.status_code = 400
    return response
