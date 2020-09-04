from django.db import models
from django.conf import settings

class Headlines(models.Model):
    title=models.CharField(max_length=120)
    image=models.ImageField()
    url=models.TextField()

class Userprofile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    last_scrape=models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return "{}-{}".format(self.user,self.last_scrape)

