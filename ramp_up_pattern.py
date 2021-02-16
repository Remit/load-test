import base64

from locust import HttpLocust, LoadTestShape, TaskSet, task
from random import randint, choice

class MyCustomShape(LoadTestShape):
    time_limit = 600
    spawn_rate = 20

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit:
            user_count = run_time
            return (user_count, spawn_rate)

        return None

class WebTasks(TaskSet):

    @task
    def load(self):
        base64string = base64.encodestring('%s:%s' % ('user', 'password')).replace('\n', '')

        catalogue = self.client.get("/catalogue").json()
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class Web(HttpLocust):
    task_set = WebTasks
    min_wait = 0
    max_wait = 0
