import unittest
import json
from flask import url_for
from api import create_app, db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertTrue(response.status_code == 404)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_task(self):
        test_task = {'title':'Smash Patriarchy'}
        
        #create task
        response = self.client.post(url_for('api.create_task'),
                         data=json.dumps(test_task),
                         content_type='application/json')
        self.assertEquals(response.status_code,201)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['title'],test_task['title'])
        inputted_id = json_response['id']

        #get task
        response = self.client.get(url_for('api.get_task',
                                   task_id = inputted_id,
                                   _external = True))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['title'],test_task['title'])

        #update task
        response = self.client.put(url_for('api.update_task',
                                           task_id = inputted_id),
                                   data=json.dumps({'done':True}),
                                   content_type='application/json')
        self.assertEquals(response.status_code,201)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['done'],True)

        #delete task
        response = self.client.delete(url_for('api.delete_task',
                                              task_id = inputted_id))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code,201)

    def test_user(self):
        test_user = {'name':'Lenin'}

        #create user
        response = self.client.post(url_for('api.create_user'),
                                   data=json.dumps(test_user),
                                   content_type='application/json')
        self.assertEquals(response.status_code,201)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'],test_user['name'])
        inputted_id = json_response['id']

        #get user
        respose = self.client.get(url_for('api.get_user',
                                          user_id = inputted_id,
                                          _external = True))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['name'],test_user['name'])

        #delete user
        response = self.client.delete(url_for('api.delete_user',
                                              user_id = inputted_id))
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertEquals(response.status_code,201)
