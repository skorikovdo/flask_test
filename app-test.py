from app import app, db
from model import *
import unittest
import os
from config import basedir
import json


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'tests.db')
        self.app = app.test_client()
        db.create_all()

    def test_1(self):
        self.app.post('/api/user/create', data=json.dumps({"name": "Sasha"}))
        self.app.post('/api/user/create', data=json.dumps({"name": "Andrey"}))
        self.app.post('/api/user/create', data=json.dumps({"name": "Georg"}))
        self.app.post('/api/user/create', data=json.dumps({"name": "Masha"}))
        user_list = self.app.get('/api/user/list')

        for user in json.loads(user_list.data):
            print('Пользователь номер ' + str(user['id']), user)

        self.app.post('/api/followers/create', data=json.dumps({"follower_id": 1, "followed_id": 3}))
        self.app.post('/api/followers/create', data=json.dumps({"follower_id": 1, "followed_id": 2}))
        self.app.post('/api/followers/create', data=json.dumps({"follower_id": 2, "followed_id": 4}))

        followers_list = self.app.get('/api/followers/list')
        follower = json.loads(followers_list.data)
        for key in follower:
            print('Пользователь', key, 'подписчик(и)', follower[key])

        self.app.post('/api/message/create', data=json.dumps({"user_id": 1, "message_text": "Hello, I am user 1"}))
        self.app.post('/api/message/create', data=json.dumps({"user_id": 2, "message_text": "Hello, I am user 2"}))
        for i in range(1, 100000000):
            pass
        self.app.post('/api/message/create', data=json.dumps({"user_id": 3, "message_text": "Hello, I am user 3"}))

        message_post = self.app.post('/api/message/post', data=json.dumps({"id": 1}))
        print(json.loads(message_post.data))

        message_time = self.app.post('/api/message/list', data=json.dumps({"id": 1}))
        message_time_for_follower = json.loads(message_time.data)
        print(message_time_for_follower)

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
