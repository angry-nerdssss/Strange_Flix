from django.db import models

# Create your models here.

#this model is to take feedback from the user
class Feedback(models.Model) :
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    def __str__(self):
        return self.name

