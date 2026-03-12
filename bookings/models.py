from django.db import models

class Booking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookings')
    studio_class = models.ForeignKey('classes.StudioClass', on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.studio_class.title} by {self.user.username} - Status: {self.status}"
