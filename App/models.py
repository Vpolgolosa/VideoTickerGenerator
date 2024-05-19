from django.db import models


class Request(models.Model):
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
