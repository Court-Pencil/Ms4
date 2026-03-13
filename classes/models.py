from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    category = models.ForeignKey('classes.Category', on_delete=models.CASCADE, related_name='studioclasses')
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    duration = models.IntegerField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='classes/', blank=True, null=True)
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

    
