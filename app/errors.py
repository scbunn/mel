from flask import jsonify, render_template, request
from .main import main

"""
These are global error handlers.  Flask will not allow error handlers for 404 or
500 at the blueprint level :(
"""


@main.app_errorhandler(404)
def not_found(e):
    if 'api/' in request.url:
        response = jsonify({'status': 404, 'error': 'not found',
                            'message': 'the resouce was not found',
                            'URI': request.url})
        response.status_code = 404
        return response

    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_error(e):
    if 'api/' in request.url:
        response = jsonify({'status': 500, 'error': 'internal error',
                            'message': 'An internal error occurred',
                            'URI': request.url})
        response.status_code = 500
        return response

    return render_template('500.html'), 500
