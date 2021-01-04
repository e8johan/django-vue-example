from django.db import models

class Todo(models.Model):
    text = models.CharField(max_length=200)
    is_done = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
