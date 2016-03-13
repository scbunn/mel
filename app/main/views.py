from flask import render_template
from . import main


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/overview', methods=['GET'])
def overview():
    return render_template('overview.html')
