from django.contrib import admin

# Register your models here.

from .models import Competition, Profile, PointSystem

admin.site.register(Competition)
admin.site.register(Profile)
admin.site.register(PointSystem)