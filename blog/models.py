from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    # author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    thumb = models.ImageField(default="hihou.gif")
    # thumb = models.ImageField(null=True, blank=True, default="けたくま朗報.gif")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    # https://kosuke-space.com/django-user-model-reference
    
class Simg(models.Model):
    jdg = models.CharField(max_length=200, default="ボタンで判定します")
    imgf = models.ImageField(default="hihou.gif")
    imgf = models.ImageField()
