import os
from locust import HttpUser, task, between 

class User(HttpUser):
    wait_time = between(1, 5)  # Adjust wait times as needed
    @task
    def mainPage(self):
        self.client.get("/")

    @task
    def post_img(self):
        with open(os.path.join('test', '0BWUTTN73V7C.jpg'), 'rb') as img1, \
                open(os.path.join('test', '1C1K8FOHA8J9.jpg'), 'rb') as img2:
            self.client.post(
                "/upload",
                data={
                    "dataset": "test_dataset",
                    "subdirectory1": "test_subdirectory1",
                    "subdirectory2": "test_subdirectory2"
                }, files={'pic_set_1': img1, 'pic_set_2': img2})

    @task
    def login(self):
        self.client.post(
            "/login", 
            data={
                    "username": "jb",
                    "password": "123456",
                })