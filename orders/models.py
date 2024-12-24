from django.db import models


class TelegramUser(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"User {self.chat_id}"
