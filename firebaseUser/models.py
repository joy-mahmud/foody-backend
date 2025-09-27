from django.db import models

# Create your models here.

class FirebaseUser(models.Model):
    ROLE_CHOICES = [('user','User'),('admin','Admin')]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default='user')
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.email
