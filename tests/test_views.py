import unittest
from app import flask_app

def add_numbers(a, b):
    return a + b

class TestAddition(unittest.TestCase):
    def test_addition(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

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
        self.check_route('/football')

    def test_formula1_route(self):
        self.check_route('/formula1')

    def test_rugby_route(self):
        self.check_route('/rugby')

    def check_route(self, route):
        response = self.app.get(route)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

if __name__ == '__main__':
    unittest.main()
