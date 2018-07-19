from app import app, db
from model import *
import unittest
import os
from config import basedir
class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join (basedir, 'test.db')
        self.app = app.test_client ()
        db.create_all ()

    def tearDown (self):
        db.session.remove ()
        db.drop_all ()

    def test_user (self):
        user1 = User(name='Andrey')
        user2 = User(name='Sasha')
        user3 = User(name='Alex')
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        andr = User.query.all()[0]
        assert andr.name == 'Andrey'

if __name__ == '__main__':
  unittest.main()