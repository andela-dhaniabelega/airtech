import json
import tempfile

from PIL import Image
from django.core.cache import cache
from rest_framework import status
from django_dynamic_fixture import G
from freezegun import freeze_time

from core.models import Flight, Ticket, User
from core.test_utils import BaseTestCase


class UserAPITest(BaseTestCase):

    def test_create_user(self):
        payload = {
            "username": "Tester",
            "first_name": "Tester",
            "last_name": "API",
            "email": "apitester@yahoo.com",
            "password": "Tester@12345678",
            "date_of_birth": "1990-11-30"
        }
        response = self.create_test_user(payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        serialized_response = json.loads(response.content)
        self.assertIsNotNone(serialized_response['token'])
        self.assertIsNotNone(serialized_response['user'])

    def test_create_user_incorrect_password(self):
        payload = {
            "username": "Tester",
            "first_name": "Tester",
            "last_name": "API",
            "email": "apitester@yahoo.com",
            "password": "tester@12345678",  # Incorrect Password
            "date_of_birth": "1990-11-30"
        }
        response = self.create_test_user(payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_incorrect_email(self):
        payload = {
            "username": "Tester",
            "first_name": "Tester",
            "last_name": "API",
            "email": "apitester@",  # Incorrect Email
            "password": "tester@12345678",
            "date_of_birth": "1990-11-30"
        }
        response = self.create_test_user(payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        payload = {
            "username": "UserLogin",
            "first_name": "Login",
            "last_name": "API",
            "email": "userlogin@yahoo.com",
            "password": "UserLogin@12345678",
            "date_of_birth": "1990-11-30"
        }
        self.create_test_user(payload)
        response = self.client.post('/api/v1/user/login/', {"username": "UserLogin", "password": "UserLogin@12345678"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_response = json.loads(response.content)
        self.assertIsNotNone(serialized_response['token'])
        self.assertIsNotNone(serialized_response['user'])

    def test_invalid_login_user(self):
        response = self.client.post('/api/v1/user/login/', {"username": "fakeuser", "password": "Fake@password123445"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        serialized_response = json.loads(response.content)
        self.assertIsNotNone(serialized_response['non_field_errors'])


class PhotoUploadTest(BaseTestCase):
    def setUp(self):
        self.payload = {
            "username": "UserLogin",
            "first_name": "Login",
            "last_name": "API",
            "email": "userlogin@yahoo.com",
            "password": "UserLogin@12345678",
            "date_of_birth": "1990-11-30"
        }
        self.create_test_user(self.payload)
        logged_in_user = self.log_in_user(username=self.payload["username"], password=self.payload["password"])
        serialized_user = json.loads(logged_in_user.content)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + serialized_user['token'])
        self.user_id = serialized_user['user']['user_id']

        # Generate an image with Pillow
        self.image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
        self.file = tempfile.NamedTemporaryFile(suffix='.png')
        self.image.save(self.file)

    def test_upload_image(self):
        with open(self.file.name, 'rb') as data:
            self.payload['photo'] = data
            url = '/api/v1/user/{}/upload_photo/'.format(self.user_id)
            response = self.client.put(url, self.payload, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_upload_image_exceed_size(self):
        self.image = Image.new('RGBA', size=(70000, 70000))
        self.file = tempfile.NamedTemporaryFile(suffix='.png')
        self.image.save(self.file)

        with open(self.file.name, 'rb') as data:
            self.payload['photo'] = data
            url = '/api/v1/user/{}/upload_photo/'.format(self.user_id)
            response = self.client.put(url, self.payload, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_image(self):
        url = '/api/v1/user/{}/upload_photo/'.format(self.user_id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        user = User.objects.get(pk=self.user_id)
        self.assertTrue('avatar' in user.photo.name)


class FlightAPITest(BaseTestCase):

    def setUp(self):
        cache.clear()
        payload = {
            "username": "UserLogin",
            "first_name": "Login",
            "last_name": "API",
            "email": "userlogin@yahoo.com",
            "password": "UserLogin@12345678",
            "date_of_birth": "1990-11-30"
        }
        self.flight = G(Flight, n=1)
        self.create_test_user(payload)
        logged_in_user = self.log_in_user(username=payload["username"], password=payload["password"])
        serialized_user = json.loads(logged_in_user.content)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + serialized_user['token'])

    def test_list_all_flights(self):
        fields = ["id", "flight_number", "depature_city", "arrival_city", "price", "gate", "status"]
        response = self.client.get('/api/v1/flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_response = json.loads(response.content)[0]
        self.verify_data(serialized_response, self.flight, fields)

    def test_create_flight(self):
        payload = {
            "depature_time": "00:07:10.752936",
            "depature_date": "2018-12-15",
            "depature_city": "London",
            "arrival_time": "00:07:10.752936",
            "arrival_date": "2018-12-15",
            "arrival_city": "Japan",
            "price": "200",
            "flight_number": "AT008"
        }
        response = self.client.post('/api/v1/flights/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_flight(self):
        url = '/api/v1/flights/{}/'.format(self.flight.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_flight_details(self):
        payload = {
            "depature_time": "00:07:10.752936",
            "depature_date": "2018-12-15",
            "depature_city": "1",
            "arrival_time": "00:07:10.752936",
            "arrival_date": "2018-12-15",
            "arrival_city": "1",
            "price": "1",
            "flight_number": "1",
            "status": "BO"  # Updated Value
        }
        url = '/api/v1/flights/{}/'.format(self.flight.id)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        serialized_updated_flight = json.loads(response.content)
        self.assertEqual(serialized_updated_flight['status'], "BO")

    def test_delete_flight(self):
        url = '/api/v1/flights/{}/'.format(self.flight.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @freeze_time("2018-12-02")
    def test_check_flight_reservations(self):
        flight = G(Flight, flight_number="AT123")
        G(Ticket, status="RD", flight_details=flight)
        G(Ticket, status="RD", flight_details=flight)
        payload = {
            "flight_number": "AT123",
            "date": "2018-12-02"
        }
        response = self.client.post('/api/v1/flights/reservations/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_response = json.loads(response.content)
        self.assertEqual(serialized_response['reservations'], 2)

    def test_check_flight_status(self):
        url = '/api/v1/flights/{}/status/'.format(self.flight.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized_response = json.loads(response.content)
        self.assertEqual(serialized_response['status'], "OT")


class TicketTestAPI(BaseTestCase):
    def setUp(self):
        payload = {
            "username": "Tester",
            "first_name": "Tester",
            "last_name": "API",
            "email": "apitester@yahoo.com",
            "password": "Tester@12345678",
            "date_of_birth": "1990-11-30"
        }
        self.user = self.create_test_user(payload)
        logged_in_user = self.log_in_user(username=payload["username"], password=payload["password"])
        self.serialized_user = json.loads(logged_in_user.content)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.serialized_user['token'])
        self.flight = G(Flight)
        self.ticket = G(Ticket)

    def test_create_ticket(self):
        payload = {
            "flight_details": self.flight.id,
            "owner": self.serialized_user['user']['user_id'],
            "ticket_status": "PD"
        }
        response = self.client.post('/api/v1/tickets/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_all_tickets(self):
        response = self.client.get('/api/v1/tickets/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ticket_details(self):
        payload = {
            "flight_details": self.flight.id,
            "owner": self.serialized_user['user']['user_id'],
            "ticket_status": "RD"  # Updated Value
        }
        url = '/api/v1/tickets/{}/'.format(self.ticket.id)
        response = self.client.put(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(url)
        serialized_updated_ticket = json.loads(response.content)
        self.assertEqual(serialized_updated_ticket['ticket_status'], "RD")

    def test_delete_ticket(self):
        url = '/api/v1/tickets/{}/'.format(self.ticket.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
