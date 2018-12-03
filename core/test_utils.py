from rest_framework.test import APITestCase


class BaseTestCase(APITestCase):

    def create_test_user(self, payload=None):
        if payload is None:
            payload = {
                "username": "Tester",
                "first_name": "Tester",
                "last_name": "API",
                "email": "apitester@yahoo.com",
                "password": "Tester@12345678",
                "date_of_birth": "1990-11-30"
            }
        return self.client.post('/api/v1/user/create/', payload)

    def log_in_user(self, username=None, password=None):
        return self.client.post('/api/v1/user/login/', {"username": username, "password": password})

    def verify_data(self, json_data, target, fields):
        for field in fields:
            self.assertEqual(json_data[field], getattr(target, field))
