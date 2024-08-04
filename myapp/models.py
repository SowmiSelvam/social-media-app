from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


# class User(AbstractUser):
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=150)
#     password = models.CharField(max_length=150)
# groups = models.ManyToManyField(
#     'auth.Group',
#     related_name='myapp_users',  # Add related_name here
#     blank=True,
#     help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
#     verbose_name='groups',
# )

# user_permissions = models.ManyToManyField(
#     'auth.Permission',
#     related_name='myapp_user_permissions',  # Add related_name here
#     blank=True,
#     help_text='Specific permissions for this user.',
#     verbose_name='user permissions',
# )


class Note(models.Model):
    id = models.AutoField(primary_key=True)  # Add an AutoField as primary key
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    user_comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'note')
