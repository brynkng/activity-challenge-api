from django.contrib import admin

# Register your models here.

from .models import Competition, Profile, PointSystem, CompetitionInvitation, CompetitionScore

admin.site.register(Competition)
admin.site.register(CompetitionInvitation)
admin.site.register(CompetitionScore)
admin.site.register(Profile)
admin.site.register(PointSystem)