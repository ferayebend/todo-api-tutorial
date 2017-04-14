import unittest
import json
from flask import url_for
from api import create_app, db
from api.models import User, Task

from test_client import TestClient

class APITestCase(unittest.TestCase):
    default_username = 'lenin'
    default_password = '1917'

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u = User(username=self.default_username,
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
        test_user = {'username':'Lenin'}

        #create user
        response, json_response = self.client.post(url_for('api.create_user'),
                                                   data=test_user)
        self.assertEquals(response.status_code,201)
        self.assertTrue(json_response['username'],test_user['username'])
        inputted_id = json_response['id']

        #get user
        respose, json_response = self.client.get(url_for('api.get_user',
                                                 user_id = inputted_id,
                                                 _external = True))
        self.assertTrue(json_response['username'],test_user['username'])

        #delete user
        response, json_response = self.client.delete(url_for('api.delete_user',
                                                     user_id = inputted_id))
        self.assertEquals(response.status_code,201)

    def test_relations(self):
        user2_json = {'username': 'durruti',
                      'password': '1938'}

        user2 = User.from_json(user2_json)
        db.session.add(user2)
        db.session.commit()

        user2_tasks = [{'title': 'destroy the state'},
                       {'title': 'form cooperatives'}]
        user1_tasks = [{'title': 'form a proletarian dictatorship'},
                       {'title': 'implement the 5 year plan'},
                       {'title': 'decide on a successor'}]

        # we put the tasks 'manually' in order to not login in and out of user1
        for task_json in user2_tasks:
            task = Task.from_json(task_json)
            task.user_id = user2.id
            db.session.add(task)
        db.session.commit()

        # create task of user1
        for task in user1_tasks:
            response, json_response = self.client.post(url_for('api.create_task'),
                                                   data=task)

        # get tasks of user1

        response, json_response = self.client.get(url_for('api.get_tasks')) 
        self.assertEquals(response.status_code, 200)

        # check if only the task of the user is given
        self.assertEquals(len(json_response['tasks']), 3)

        response_titles = [task['title'] for task in json_response['tasks']]
        input_titles = [task['title'] for task in user1_tasks]

        self.assertEquals(set(input_titles), set(response_titles))
