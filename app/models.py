from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=1000)

class Post(models.Model):
    TimeStamp = models.DateTimeField(auto_now_add=True)
    header_img=models.FileField(null=True,blank=True,upload_to="images/")
    Title = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Experience = models.TextField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
