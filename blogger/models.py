from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profilePhoto = models.ImageField(null=True, upload_to='img/', verbose_name="Image")
    introduction = models.CharField(max_length=50, null=True)
    pass


class Message(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    content = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)
    show = models.BooleanField(default=True)
    pic = models.ImageField(null=True, upload_to='img/', verbose_name="Image", blank=True)
    o_ID = models.CharField(max_length=10, null=True, blank=True)


class Comment(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, to_field='ID', verbose_name="messageID",related_name='cm')
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    content = models.CharField(max_length=140)


class Cikes(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='ID', verbose_name="commentID",related_name="cl")
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    time = models.DateTimeField(auto_now_add=True)


class Mlikes(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, to_field='ID', verbose_name="messageID",related_name='ml')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    time = models.DateTimeField(auto_now_add=True)


class Collect(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, to_field='ID', verbose_name="messageID",related_name='cl')
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    time = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username",
                                  related_name="following")
    fans = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username",
                             related_name="fans")
    ID = models.BigAutoField(primary_key=True, editable=False)


class Background(models.Model):
    back = models.CharField(max_length=50, default='white')
    music = models.FileField(null=True, blank=True)
    ID = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username")
    Font_color = models.CharField(max_length=50, default='black')
    Border_color = models.CharField(max_length=50, default='white')


class Notice(models.Model):
    ID = models.BigAutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username', verbose_name="username",related_name='nt')
    likes = models.IntegerField(default=0)
    relays = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    fans = models.IntegerField(default=0)

