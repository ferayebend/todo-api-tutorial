import unittest
import json
from flask import url_for
from api import create_app, db
from api.models import User

from test_client import TestClient

class APITestCase(unittest.TestCase):
    default_username = 'lenin'
    default_password = '1917'

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u = User(name=self.default_username,
                 password=self.default_password)
        db.session.add(u)
        db.session.commit()

        self.client = TestClient(self.app, u.generate_auth_token(),'')

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response, json_response = self.client.get('/wrong/url')
        self.assertTrue(response.status_code == 404)
        self.assertTrue(json_response['error'] == 'not found')

    def test_task(self):
        test_task = {'title':'Smash Patriarchy'}
        
        #create task
        response, json_response = self.client.post(url_for('api.create_task'),
                         data=test_task)
        self.assertEquals(response.status_code,201)
        self.assertTrue(json_response['title'],test_task['title'])
        inputted_id = json_response['id']

        #get task
        response, json_response = self.client.get(url_for('api.get_task',
                                                  task_id = inputted_id,
                                                   _external = True))
        self.assertTrue(json_response['title'],test_task['title'])

        #update task
        response, json_response = self.client.put(url_for('api.update_task',
                                                  task_id = inputted_id),
                                                  data={'done':True})
        self.assertEquals(response.status_code,201)
        self.assertTrue(json_response['done'],True)

        #delete task
        response, json_response = self.client.delete(url_for('api.delete_task',
                                                     task_id = inputted_id))
        self.assertEquals(response.status_code,201)

    def test_user(self):
        test_user = {'name':'Lenin'}

        #create user
        response, json_response = self.client.post(url_for('api.create_user'),
                                                   data=test_user)
        self.assertEquals(response.status_code,201)
        self.assertTrue(json_response['name'],test_user['name'])
        inputted_id = json_response['id']

        #get user
        respose, json_response = self.client.get(url_for('api.get_user',
                                                 user_id = inputted_id,
                                                 _external = True))
        self.assertTrue(json_response['name'],test_user['name'])

        #delete user
        response, json_response = self.client.delete(url_for('api.delete_user',
                                                     user_id = inputted_id))
        self.assertEquals(response.status_code,201)

