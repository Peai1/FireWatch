from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Search(models.Model):
    address = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

class Comment(models.Model):
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s | %s' % (self.comment_body, self.commenter_name, self.date_added)
