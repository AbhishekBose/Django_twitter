from django.db import models
from django.conf import settings
import random 

# User = settings.AUTH_USER_MODEL
# Create your models here.
class Tweet(models.Model):
    # id (Autofield with primary key = True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)  #any users will have many users
    # user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL) #this can also be used if we want to have a backup in our production database
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to="images/",blank=True,null=True)

    # def __str__(self): #String representation of the obj
        # return self.content

    class Meta:
        ordering = ["-id"]
    def serialize(self):
        return {
            "id":self.id,
            "content":self.content,
            "likes":random.randint(0,200)
        }