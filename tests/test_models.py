import unittest
from api import create_app, db

from api.models import Task, User

TEST_TASKS = [
                {
                'title': u'Buy groceries',
                'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
                },
                {
                'title': u'Learn Python',
                'description': u'Need to find a good Python tutorial on the web', 
                }
             ]

TEST_USERS = [
                {
                'username': u'user1',
                },
                {
                'username': u'user2',
                }
             ]

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        for test_user in TEST_USERS:
            user = User.from_json(test_user)
            db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
        test_user_dict = TEST_USERS[0]
        user_in_db = User.query.filter_by(username=test_user_dict.get('username')).first()
        self.assertEqual(user_in_db.username, 
                         test_user_dict.get('username'))
    def test_to_json(self):
        test_user_dict = TEST_USERS[0]
        expected_keys = ['url', 'id', 'username']
        user = User.query.filter_by(username = test_user_dict.get('username')).first()
        user_json = user.to_json()
        self.assertEqual(sorted(expected_keys),sorted(user_json.keys()))
        #self.assertTrue('api/v1.0/users' in user_json.get('url'))

class TaskModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        for test_task in TEST_TASKS:
            task = Task.from_json(test_task)
            db.session.add(task)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create(self):
        test_task_dict = TEST_TASKS[0]
        '''
        task = Task.from_json(test_task_dict)
        db.session.add(task)
        db.session.commit()
        '''
        task_in_db = Task.query.filter_by(title=test_task_dict.get('title')).first()
        self.assertEqual(task_in_db.description, 
                         test_task_dict.get('description'))

    def test_to_json(self):
        test_task_dict = TEST_TASKS[0]
        expected_keys = ['url', 'id', 'title', 'description', 'done']
        task = Task.query.filter_by(title = test_task_dict.get('title')).first()
        task_json = task.to_json()
        self.assertEqual(sorted(expected_keys),sorted(task_json.keys()))
        self.assertTrue('api/v1.0/tasks', task_json.get('url'))
