from django.db import models
from django.db.models.fields import CharField

# Create your models here.


class Cars(models.Model):
    name = models.CharField(max_length=30)
    discription = models.TextField(max_length=2000)
    model = models.CharField(max_length=30)
    price = models.IntegerField(max_length=30)
    year = models.IntegerField(max_length=30)

    
class CarsImages(models.Model):
    images = models.FileField(upload_to='images/')
    cars = models.ForeignKey(Cars,related_name='images',on_delete=models.CASCADE)

class Comment(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=50)
    email = models.EmailField()
    



