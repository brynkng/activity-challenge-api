from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class PointSystem(models.Model):
    active_minute_points = models.IntegerField(default=2)
    fat_zone_points = models.IntegerField(default=0)
    cardio_zone_points = models.IntegerField(default=1)
    peak_zone_points = models.IntegerField(default=2)

    def __str__(self):
        return f"active: {self.active_minute_points} fat zone: {self.fat_zone_points} cardio zone: {self.cardio_zone_points} peak zone: {self.peak_zone_points}"

class Competition(models.Model):
    DAILY = 'DL'
    WEEKLY = 'WL'
    MONTHLY = 'ML'

    COMPETITION_TYPES = (
        (DAILY, 'Daily'),
        (WEEKLY, 'Weekly'),
        (MONTHLY, 'Monthly'),
    )

    type = models.CharField(
        max_length=2,
        choices=COMPETITION_TYPES,
        default=DAILY,
    )

    start = models.DateTimeField()

    point_system = models.ForeignKey(PointSystem, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{dict(self.COMPETITION_TYPES).get(self.type)} starting on {self.start}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=250, blank=True)

    competitions = models.ManyToManyField(Competition)

    def __str__(self):
        return f"tagline: {self.tagline} user:{user.id}"


#Signals

# Possible anti-pattern - move to creation process?
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()