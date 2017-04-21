import unittest
from flask import url_for, jsonify
from api import create_app, db
from api.models import User
from api.tasks import async

from test_client import TestClient

from time import sleep

class CeleryTestCase(unittest.TestCase):
    default_username = 'lenin'
    default_password = '1917'

    def setUp(self):
        self.app = create_app('testing')

        # add an additional route used only in tests
        @self.app.route('/foo')
        @async
        def foo():
            1 / 0

        @self.app.route('/test-long')
        @async
        def long_task():
            sleep(10)
            return jsonify({}), 200

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.drop_all()  # just in case
        db.create_all()
        u = User(username=self.default_username,
                 password=self.default_password)

        self.client = TestClient(self.app, u.generate_auth_token(),'')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_celery(self):
        response, json_response = self.client.get('/test-long')
        self.assertEquals(response.status_code,202)
        #print(json_response['Location'])
        #response, json_response = self.client.get(url_for('tasks.get_status',id=1))
        #self.assertEquals(response.status_code,202)
