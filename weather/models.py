from django.db import models

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    chat_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.chat_id})"
