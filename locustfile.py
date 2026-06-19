from locust import HttpUser, task, between

class GameDexUser(HttpUser):
    host = "https://gamedex-8uhb.onrender.com"
    wait_time = between(1, 3)

    @task(3)
    def home(self):
        self.client.get("/")

    @task(2)
    def productos(self):
        self.client.get("/productos/")

    @task(1)
    def login(self):
        self.client.post("/login/", {
            "username": "test",
            "password": "test"
        })