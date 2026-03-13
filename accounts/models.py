from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='accounts')
    bio = models.TextField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

