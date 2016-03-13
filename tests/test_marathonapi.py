import unittest
import json
from flask import current_app
from app import create_app
from app.Models import MarathonApiEvent
from app.api_v1_0 import EVENT_BUFFERS as eb


class MarathonApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def generate_event(self):
        e = MarathonApiEvent()
        e.import_data(
            MarathonApiEvent.generate_fake_event())
        return e

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_testing_config(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_marathon_api_event_model(self):
        e = self.generate_event()
        self.assertEquals(e.id, 1)
        self.assertIsNotNone(e.timestamp)
        self.assertIsNotNone(e.raw_event)
        self.assertIsNotNone(e.client)
        self.assertIsNotNone(e.app_id)
        self.assertIsNotNone(e.health_checks)
        self.assertEquals(e.event_type, 'api_post_event')
        self.assertDictEqual(e.env, {'DEBUG': True})
        self.assertEqual(2, len(e.ports), "There should be two ports")

    def test_marathon_api_get_empty(self):
        rv = self.client.get(
            '/api/v1.0/marathon/events/',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 200)
        data = json.loads(rv.get_data(as_text=True))
        self.assertListEqual([], data['events'])

    def test_marathon_api_invalid_event(self):
        rv = self.client.post(
            '/api/v1.0/marathon/events/',
            data={'message': 'invalid event'},
            content_type='application/json',
            follow_redirects=True
        )
        self.assertTrue(rv.status_code == 400)

    def test_marathon_api_post_event(self):
        rv = self.client.post(
            '/api/v1.0/marathon/events/',
            data=json.dumps(MarathonApiEvent.generate_fake_event()),
            content_type='application/json',
            follow_redirects=True
        )
        self.assertTrue(rv.status_code == 201)

        rv = self.client.get(
            '/api/v1.0/marathon/events/',
            follow_redirects=True)
        self.assertTrue(rv.status_code == 200)
        self.assertTrue(eb['marathon_events'].get_size() == 1)

    def test_marathon_api_post_multi_events(self):
        for et in range(1, 2048):
            rv = self.client.post(
                '/api/v1.0/marathon/events/',
                data=json.dumps(MarathonApiEvent.generate_fake_event()),
                content_type='application/json',
                follow_redirects=True
            )
            self.assertTrue(rv.status_code == 201)

            rv = self.client.get(
                '/api/v1.0/marathon/events/',
                follow_redirects=True)
            self.assertTrue(rv.status_code == 200)
            data = rv.get_data(as_text=True)
            self.assertTrue('api_post_event' in data)

        self.assertTrue(eb['marathon_events'].get_size() == 1024)
