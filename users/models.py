from PIL import Image
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE , related_name='profile')
    about = models.CharField(max_length=850 , null=True , blank=True)
    picture = models.ImageField(upload_to='profile-pictures' , default ='profile-pictures/default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self):
        super().save()
        img = Image.open(self.picture.path)
        # compress the profile picture
        if img.height > 300 or img.width > 300:
            img.thumbnail((300 , 300))
            img.save(self.picture.path)
