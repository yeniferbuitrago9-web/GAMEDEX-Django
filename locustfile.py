from locust import HttpUser, task, between

class GamedexPublicUser(HttpUser):
    # Tiempo de espera para que la base de datos en Render procese con calma
    wait_time = between(2, 5)

    @task(2)
    def index_page(self):
        # Prueba de carga en la página principal de Gamedex
        self.client.get("/")

    @task(1)
    def login_interface(self):
        # Prueba de carga solicitando la interfaz visual del Login
        self.client.get("/login/")