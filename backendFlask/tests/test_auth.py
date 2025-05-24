import unittest
from backendFlask import create_app, db
from backendFlask.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        test_config = {
            'TESTING': True,
            'SECRET_KEY': 'test-secret-key',
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_and_login(self):
        # Register user
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 201)

        # Login user
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 200)
        access_token = response.get_json()['access_token']

        # Access protected route
        response = self.client.get(
            '/protected',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome testuser', response.get_json()['message'])


if __name__ == '__main__':
    unittest.main()
