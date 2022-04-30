from django.urls import path

from .views import upload_file, answers_and_users

app_name = "csv_reader"

urlpatterns = [
    path("", upload_file, name="index"),
    path("user_answers/", answers_and_users, name="answers"),
]
