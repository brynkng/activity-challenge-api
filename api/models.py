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

    start = models.DateField()

    length = models.IntegerField(help_text="e.g. Daily * 5 length = 5 days")

    name = models.CharField(max_length=255)

    point_system = models.ForeignKey(PointSystem, on_delete=models.CASCADE, default=1)
    
    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tagline = models.CharField(max_length=250, blank=True)
    access_token = models.CharField(max_length=500, blank=True)
    refresh_token = models.CharField(max_length=500, blank=True)
    token_expiration = models.DateTimeField(blank=True, null=True)
    fitbit_user_id = models.CharField(max_length=50, blank=True)

    competitions = models.ManyToManyField(Competition, blank=True)

    def __str__(self):
        return f"Tagline: {self.tagline} User: {self.user.username}"


class CompetitionInvitation(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    accepted = models.BooleanField(blank=True, null=True)
    token = models.CharField(max_length=250, blank=True, null=True)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender_profile')

#Signals

# Possible anti-pattern - move to creation process?
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()