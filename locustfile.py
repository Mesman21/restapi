from locust import HttpUser, task, between

class LibraryUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_all_books(self):
        with self.client.get("/books/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed! Status code: {response.status_code}")