from django.db import models

class Category(models.Model):
    name= models.CharField(max_length=50)
    slug= models.SlugField(max_length=50)
    description = models.TextField(max_length=255, null=True, blank=True)

    #did you migrate

    def __str__(self):
        return self.name

class StudioClass(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    instructor = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    duration = models.CharField(max_length=20)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=255)
    description = models.TextField(max_length=255, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property
    def spots_remaining(self):
        return self.capacity - self.bookings.filter(status='confirmed').count()
    
    @property
    def is_full(self):
        return self.spots_remaining == 0
       

