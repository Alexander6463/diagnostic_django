from django.db import models

# Create your models here.


class User(models.Model):
    time_create = models.DateTimeField()
    time_changed = models.DateTimeField()
    name = models.CharField(max_length=150)
    group = models.CharField(max_length=50)
    member_gz_2021_2022 = models.CharField(max_length=10, null=True)
    sex = models.CharField(max_length=10)
    age = models.IntegerField()
    marital_status = models.CharField(max_length=20)
    living = models.CharField(max_length=50)
    children = models.CharField(max_length=20)
    work_status = models.CharField(max_length=50)


class Question(models.Model):
    text_question = models.TextField()


class Answers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
