import unittest
from api import create_app, db

from api.models import User

TEST_USERS = [
                {
                'name': u'user1',
                },
                {
                'name': u'user2',
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
        user_in_db = User.query.filter_by(name=test_user_dict.get('name')).first()
        self.assertEqual(user_in_db.name, 
                         test_user_dict.get('name'))
    def test_to_json(self):
        test_user_dict = TEST_USERS[0]
        expected_keys = ['url', 'id', 'name']
        user = User.query.filter_by(name = test_user_dict.get('name')).first()
        user_json = user.to_json()
        self.assertEqual(sorted(expected_keys),sorted(user_json.keys()))
        #self.assertTrue('api/v1.0/users' in user_json.get('url'))
