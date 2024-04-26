from django.db import models
from CustomUser.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.validators import RegexValidator


class ValidationAuthority(models.Model):
    phone_number_regex=RegexValidator(
        regex=r'^(\+977)?\d{9,10}$',
        message="Phone number must be entered in the format: '+977'. Up to 10 digits allowed."
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    name=models.CharField(max_length=100)
    contact=models.CharField(validators=[phone_number_regex],max_length=14,blank=True)
    class Meta:
        verbose_name='ValidationAuthority'
        verbose_name_plural='ValidationAuthority List'
    def __str__(self) -> str:
        return f"{self.name}"

def get_complain_image_upload_path(instance,filename):
    return f'complain/{filename}'

class UserComplain(models.Model):
    SEVERITY_CHOICES = (
        ('very_minimum', 'Very Minimum'),
        ('low', 'Low'),
        ('high', 'High'),
        ('very_high', 'Very High'),
    )
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    complain_user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_complain_image_upload_path)
    description = models.TextField()
    severity_level = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    solved=models.BooleanField(default=False)
    date_of_complain = models.DateTimeField(auto_now_add=True)
    solved_date=models.DateTimeField(null=True, blank=True)
    validated_by=models.ForeignKey(ValidationAuthority,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return f"Complain #{self.id}"
    
    
