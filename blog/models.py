from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="posts")
    title = models.CharField(max_length=80)
    content = models.TextField(blank=True , null=True)
    image = models.ImageField(upload_to="posts_images" , blank=True , null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author.username} | {self.created_date}"
    
    #compress the image 
    def save(self , *args , **kwargs):
        super().save()
        image = Image.open(self.image.path)
        if image.height > 700 or image.width > 700:
            image.thumbnail((700 , 700))
            image.save(self.image.path)



class PostComment(models.Model):
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="post_comments")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments")
    comment = models.CharField(max_length=1200)


class PostLikes(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="liked_posts")
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="likes")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('post' , 'user')]