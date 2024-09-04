from django.db import models


# Create your models here.
class Dance(models.Model):
    file = models.FileField(upload_to='dance/')
    upload_time = models.DateTimeField(auto_now=True)


class Music(models.Model):
    dance = models.ForeignKey(Dance, on_delete=models.CASCADE)
    file = models.FileField(upload_to='music/', null=True)
    combine = models.FileField(upload_to='combine/', null=True)
    completed = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now=True)


class DanceFeature(models.Model):
    file_name = models.CharField(max_length=50)
    style = models.CharField(max_length=20, null=True)
    file = models.FileField(upload_to='dance_feature/')


class MusicSeed(models.Model):
    file_name = models.CharField(max_length=50)
    style = models.CharField(max_length=20, null=True)
    file = models.FileField(upload_to='music_seed/')
