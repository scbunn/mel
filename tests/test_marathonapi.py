import unittest
import json
from flask import current_app
from app import create_app
from app.Models import MarathonEventBase, MarathonEvent
from app.api_v1_0 import MARATHON_EVENTS as mbuf


class DummyRequest(object):
    """Dummy request object"""

    def __init__(self):
        # TODO: figure out a better way to do this!
        self.json = MarathonEventBase.generate_fake_event()
        self.remote_addr = '127.0.0.1'


class MarathonApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_testing_config(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_api_model(self):
        e = MarathonEvent()
        e.import_data(DummyRequest())
        self.assertIsNotNone(e.id)
        self.assertIsNotNone(e.timestamp)
        self.assertIsNotNone(e.marathon_host)
        self.assertIsNotNone(e.eventType)
        self.assertIsNotNone(e.event)

    def test_api_get_empty(self):
        rv = self.client.get(
            '/api/v1.0/events/',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 200)
        data = json.loads(rv.get_data(as_text=True))
        self.assertListEqual([], data['events'])

    def test_api_invalid_event(self):
        rv = self.client.post(
            '/api/v1.0/events/',
            data={'message': 'invalid event'},
            content_type='application/json',
            follow_redirects=True
        )
        self.assertTrue(rv.status_code == 400)

    def test_api_post_event(self):
        rv = self.client.post(
            '/api/v1.0/events/',
            data=json.dumps(MarathonEventBase.generate_fake_event()),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertTrue(rv.status_code == 201)

        rv = self.client.get(
            '/api/v1.0/events/',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(mbuf.get_size() == 1)

    def test_api_post_multi_events(self):
        for et in range(1, 1030):
            rv = self.client.post(
                '/api/v1.0/events/',
                data=json.dumps(MarathonEventBase.generate_fake_event()),
                content_type='application/json',
                follow_redirects=True
            )
            self.assertTrue(rv.status_code == 201)

            rv = self.client.get(
                '/api/v1.0/events/',
                follow_redirects=True)
            self.assertTrue(rv.status_code == 200)
            data = rv.get_data(as_text=True)
            self.assertTrue('api_post_event' in data)

        self.assertTrue(mbuf.get_size() == 1024)
