from django.db import models
from CustomUser.models import User

class Event(models.Model):
    title=models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images')
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    signed_users = models.ManyToManyField(User,blank=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title