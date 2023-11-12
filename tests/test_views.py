import unittest
from app import flask_app

def add_numbers(a, b):
    return a + b

class SanityTest(unittest.TestCase):
    def test_addition(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)
        
class TestPostFeature(unittest.TestCase):
    def setUp(self):
        self.app = flask_app().test_client()
        self.login()

    def login(self):
        return self.app.post('/login', data=dict(
            username='testuser',
            password='Testpassword1'
        ), follow_redirects=True)
        
    def test_create_post(self):
        response = self.app.post('/football-post', data={'post': 'This is a new football post.'})
        self.assertEqual(response.status_code, 302)
        
    def test_add_comment(self):
        response = self.app.post('/add-comment/football/1', data={'content': 'This is a comment.'})
        self.assertEqual(response.status_code, 302)

class TestOverviewRoute(unittest.TestCase):
    def setUp(self):
        self.app = flask_app().test_client()

    def test_overview_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Sup<i class="fa-regular fa-futbol"></i>rt', response.data)
        
class TestSportsRoutes(unittest.TestCase):
    def setUp(self):
        self.app = flask_app().test_client()

    def test_football_route(self):
        self.check_route('/football-post')

    def test_formula1_route(self):
        self.check_route('/formula1-post')

    def test_rugby_route(self):
        self.check_route('/rugby-post')

    def check_route(self, route):
        response = self.app.get(route)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

if __name__ == '__main__':
    unittest.main()
