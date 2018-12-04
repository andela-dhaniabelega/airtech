import json

from locust import HttpLocust, TaskSet, task


class UserActions(TaskSet):

    def __init__(self, parent):
        super(UserActions, self).__init__(parent)

        self.token = ""
        self.headers = {}

    def on_start(self):
        self.token = self.login()

        self.headers = {'Authorization': 'JWT ' + self.token}

    def login(self):
        auth_response = self.client.post('http://localhost:8000/api/v1/user/login/',
                                         {'username': 'Salika', 'password': 'Loyola@12345678'})
        auth_token = json.loads(auth_response.content)['token']
        return auth_token

    @task(1)
    def add_flight_api(self):
        data = {
            "depature_time": "00:07:10.752936",
            "depature_date": "2018-12-01",
            "depature_city": "London",
            "arrival_time": "00:07:10.752936",
            "arrival_date": "2018-12-01",
            "arrival_city": "Austin",
            "price": "200",
            "flight_number": "ATT5436"
        }
        self.client.post('http://localhost:8000/api/v1/flights/', data, headers=self.headers)

    @task(2)
    def update_flight_api(self):
        data = {
            "depature_time": "00:07:10.752936",
            "depature_date": "2018-12-01",
            "depature_city": "London",
            "arrival_time": "00:07:10.752936",
            "arrival_date": "2018-12-01",
            "arrival_city": "Austin",
            "price": "400",
            "flight_number": "AT3456"
        }
        self.client.put('http://localhost:8000/api/v1/flights/8/', data, headers=self.headers)

    @task(3)
    def retrieve_flight_api(self):
        self.client.get('http://localhost:8000/api/v1/flights/', headers=self.headers)

    @task(4)
    def add_ticket_api(self):
        data = {
            "flight_details": 8,
            "owner": 21,
            "ticket_status": "PD"
        }
        self.client.post('http://localhost:8000/api/v1/tickets/', data, headers=self.headers)

    @task(5)
    def update_ticket_api(self):
        data = {
            "flight_details": 8,
            "owner": 21,
            "ticket_status": "RD"
        }
        self.client.put('http://localhost:8000/api/v1/tickets/17/', data, headers=self.headers)

    @task(6)
    def retrieve_ticket_api(self):
        self.client.get('http://localhost:8000/api/v1/tickets/', headers=self.headers)


class ApplicationUser(HttpLocust):
    task_set = UserActions
    min_wait = 0
    max_wait = 0
