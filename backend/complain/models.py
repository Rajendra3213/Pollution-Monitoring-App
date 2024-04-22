from django.db import models
from CustomUser.models import User

def get_complain_image_upload_path(instance,filename):
    return f'complain/{filename}'

class UserComplain(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_complain_image_upload_path)
    description = models.TextField()
    date_of_complain = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complain #{self.id}"
