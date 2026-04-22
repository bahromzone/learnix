from locust import HttpUser, task

class WebsiteUser(HttpUser):
    def on_start(self):
        self.token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1bWFyQGdtYWlsLmNvbSIsImV4cCI6MTc0ODI3OTAyNywidG9rZW5fdHlwZSI6ImFjY2VzcyJ9.-SaZNUlHwDIEuNxgv97gBDfctDBVxlJ39rktwyMo0cs"

    @task
    def get_students(self):
        headers = {"Authorization": self.token}
        self.client.get("/student/get_all_students", headers=headers)
