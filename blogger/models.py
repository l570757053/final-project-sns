import collections
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ProfilePhoto=models.ImageField(null=True,upload_to='img/',verbose_name="Image")
    introduction=models.CharField(max_length=50,default=None)
    pass


class message(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    content=models.CharField(max_length=140)
    time=models.DateTimeField(auto_now_add=True)
    show=models.BooleanField(default=True)
    pic=models.ImageField(null=True,upload_to='img/',verbose_name="Image")
    o_ID=models.CharField(default=None,max_length=10)


class comment(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    message_id=models.ForeignKey(message,on_delete=models.CASCADE,to_field='ID',verbose_name="messageID")
    time=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    content=models.CharField(max_length=140)



class clikes(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    comment_id=models.ForeignKey(comment,on_delete=models.CASCADE,to_field='ID',verbose_name="commentid")
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    time=models.DateTimeField(auto_now_add=True)


class mlikes(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    message_id=models.ForeignKey(message,on_delete=models.CASCADE,to_field='ID',verbose_name="messageid")
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    time=models.DateTimeField(auto_now_add=True)

class collect(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    message_id=models.ForeignKey(message,on_delete=models.CASCADE,to_field='ID',verbose_name="messageid")
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    time=models.DateTimeField(auto_now_add=True)

class follow(models.Model):
    following=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username", related_name="following")
    fans=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username" ,related_name="fans")
    ID=models.BigAutoField(primary_key=True,editable=False)

class background(models.Model):
    back=models.CharField(max_length=50,default='white')
    music=models.FileField()
    ID=models.BigAutoField(primary_key=True,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    Fontcolor=models.CharField(max_length=50,default='black')
    Bordercolor=models.CharField(max_length=50,default='white')




class notice(models.Model):
    ID=models.BigAutoField(primary_key=True,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',verbose_name="username")
    likes=models.IntegerField(default='0')
    relays=models.IntegerField(default='0')
    comments=models.IntegerField(default='0')
    fans=models.IntegerField(default='0')



