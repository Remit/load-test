import base64

from locust import HttpUser, TaskSet, task, constant
from random import randint, choice


class WebTasks(TaskSet):

    @task
    def load(self):

        data_string = '{}:{}'.format('user', 'password')
        data_bytes = data_string.encode('utf-8')
        base64string = base64.b64encode(data_bytes)

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization": 'Basic {}'.format(base64string)})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class Web(HttpUser):
    wait_time = constant(5)
    tasks = {WebTasks:10}
