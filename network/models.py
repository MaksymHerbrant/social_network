from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(upload_to='network/static/img/avatar/', null=True, blank=True)
    about = models.CharField(max_length=100,null=True,blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    hobby = models.CharField(max_length=30,null=True,blank=True)
    work = models.CharField(max_length=30,null=True,blank=True)
    city = models.CharField(max_length=25,null=True,blank=True)





class Post(models.Model):
    title = models.CharField(max_length=100)
    
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='network/static/img/photo/',null=True,blank=True)

    
    
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = models.ImageField(upload_to='static/img/avatars', null=True, blank=True)
    
#     def __str__(self):
#  
# 
#        return self.user.username

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)


class Follow(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    following = models.ManyToManyField(User,related_name='following')
    followers = models.ManyToManyField(User,related_name='followers')
    def __str__(self):
        return self.user.username
    

class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='members')
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=10000)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)

