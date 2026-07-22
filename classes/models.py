from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from datetime import datetime, timedelta

class Category(models.Model):
    name= models.CharField(max_length=50)
    slug= models.SlugField(max_length=50)
    description = models.TextField(max_length=255, null=True, blank=True)
   
    class Meta:
        verbose_name_plural = "Categories"

    #did you migrate

    def __str__(self):
        return self.name

class StudioClass(models.Model):
    title = models.CharField(max_length=100)
    slug= models.SlugField(max_length=50, blank=True, null=True)
    category = models.ForeignKey('classes.Category', on_delete=models.CASCADE, related_name='studioclasses')
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.IntegerField()
    start_time = models.TimeField(null=True, blank=True)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='classes/', blank=True, null=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    @property
    def spots_remaining(self):
        booked = self.bookings.filter(status='confirmed').count()
        remaining = self.capacity - booked
        return max(0, remaining)
    
    @property
    def is_full(self):
        return self.spots_remaining == 0
    
    @property
    def duration_display(self):
        hours = self.duration // 60
        minutes = self.duration % 60
        if hours > 0 and minutes > 0:
            return f"{hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"
        
    @property
    def end_time(self):
        if self.start_time:
            start_datetime = datetime.combine(self.date, self.start_time)
            end_datetime = start_datetime + timedelta(minutes=self.duration)
            return end_datetime.time()
        return None

    def save(self, *args, **kwargs):
         self.slug = slugify(self.title, allow_unicode=False) 
         super().save()
    
    class Meta:
        verbose_name_plural = "Studio Classes"

    
    
class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='reviews')
    studio_class = models.ForeignKey('classes.StudioClass', on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.studio_class.title} by {self.user.username} - {self.created_at}"
       
    class Meta:
        unique_together = ('user', 'studio_class')
        verbose_name_plural = 'Reviews'

    
