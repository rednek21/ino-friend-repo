from django.db import models


class FeedBack(models.Model):
    code = models.UUIDField(unique=True)
    name = models.CharField(max_length=32)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f'FeedBack object {self.code}'
