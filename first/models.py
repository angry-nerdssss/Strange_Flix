from django.db import models
from datetime import datetime
from datetime import date
from django.contrib.auth.models import User

# Create your models here.

#this model is to take feedback from the user
class Feedback(models.Model) :
    name = models.CharField(max_length=100)
    publish_date = models.DateField(auto_now_add=True)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    def __str__(self):
        return self.name

#this model is designed to make,update and renew the subscription of the use to the site
class Subscription(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    paid = models.CharField(max_length=20,default=False)
    deadline=models.DateField(default=datetime.today)
    def __str__(self):
        return self.paid