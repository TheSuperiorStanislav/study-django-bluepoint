from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Blog(models.Model):
    owner = models.ForeignKey(User, editable = False, on_delete=models.CASCADE)
    title = models.CharField(max_length = 500)

    slug = models.CharField(max_length = 500, editable = False)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length = 500)
    body = models.TextField(default='')
    shared_to = models.ManyToManyField(Blog,related_name='shared_posts')

    is_published = models.BooleanField(default=False)

    slug = models.CharField(max_length = 500, editable = False)

    def __str__(self):
        return self.title
    
